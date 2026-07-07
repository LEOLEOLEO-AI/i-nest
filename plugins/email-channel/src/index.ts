/**
 * OpenClaw Email Channel Plugin
 *
 * Registers "email" as a native channel with:
 * - HTTP route POST /api/email/inbound for receiving emails from backend
 * - Outbound adapter sendText() for delivering agent replies via backend MailChannels
 * - Proper MsgContext with OriginatingChannel/OriginatingTo for native reply routing
 *
 * Flow:
 *   Backend POST → /api/email/inbound → plugin parses + dispatches to agent
 *   → agent replies → Gateway routeReply("email") → plugin sendText()
 *   → POST backend /api/openclaw/email/send → MailChannels → recipient inbox
 *
 * Single-file layout (matches genspark-im pattern). OpenClaw >= 2026.5.x's
 * runtime warns about cross-file imports without compiled `dist/` output;
 * keeping everything in one entry file avoids needing a build step.
 */

import { createHash } from "crypto";
import { readFile, writeFile, mkdir, access, realpath } from "fs/promises";
import { dirname, basename, extname } from "path";
import { constants } from "fs";
import { createServer } from "http";
import type { IncomingMessage, ServerResponse } from "http";

// ---------------------------------------------------------------------------
// Config from environment (injected by VM configure script)
// ---------------------------------------------------------------------------

const EMAIL_SEND_URL = process.env.OPENCLAW_EMAIL_SEND_URL || "";
const EMAIL_SECRET = process.env.OPENCLAW_EMAIL_SECRET || "";
const EMAIL_ADDRESS = process.env.OPENCLAW_EMAIL_ADDRESS || "";
const VM_NAME = process.env.OPENCLAW_VM_NAME || "";

// ---------------------------------------------------------------------------
// Plugin runtime singleton — set during register(), used by inbound handler.
// ---------------------------------------------------------------------------

let runtime: any = null;

function setEmailRuntime(next: any) {
  runtime = next;
}

function getEmailRuntime(): any {
  if (!runtime) {
    throw new Error("Email plugin runtime not initialized");
  }
  return runtime;
}

// ---------------------------------------------------------------------------
// Persistent store for email thread metadata (subject + messageId).
//
// Problem: OpenClaw uses MessageThreadId as part of the session filename.
// When MessageThreadId contains URL-encoded Chinese subjects and long
// Outlook Message-IDs, the filename exceeds Linux's 255-byte limit.
//
// Solution: Use a short hash as the MessageThreadId and store the full
// thread info (subject + messageId) in a JSON file on disk.
// ---------------------------------------------------------------------------

type ThreadInfo = {
  subject: string;
  messageId: string;
  /** Original email body for quoting in replies */
  originalBody?: string;
  /** Sender of the original email (for attribution in quote) */
  originalFrom?: string;
  /** Timestamp of the original email */
  originalDate?: string;
  /** VM was CC'd/BCC'd only — absorb context, suppress reply */
  ccOnly?: boolean;
};

const threadCache = new Map<string, ThreadInfo>();
const STORE_DIR = process.env.OPENCLAW_DATA_DIR || "/home/work/.openclaw";
const STORE_PATH = `${STORE_DIR}/agents/main/email-thread-info.json`;

function threadKey(subject: string, messageId: string): string {
  const input = JSON.stringify({ subject, messageId });
  return createHash("sha256").update(input).digest("hex").slice(0, 12);
}

async function loadDiskStore(): Promise<Record<string, ThreadInfo>> {
  try {
    const raw = await readFile(STORE_PATH, "utf-8");
    return JSON.parse(raw);
  } catch {
    return {};
  }
}

async function storeThreadInfo(
  subject: string,
  messageId: string,
  extra?: { originalBody?: string; originalFrom?: string; originalDate?: string; ccOnly?: boolean },
): Promise<string> {
  const key = threadKey(subject, messageId);
  const info: ThreadInfo = { subject, messageId, ...extra };
  threadCache.set(key, info);

  if (threadCache.size > 500) {
    const iter = threadCache.keys();
    for (let i = threadCache.size - 500; i > 0; i--) {
      threadCache.delete(iter.next().value!);
    }
  }

  try {
    const existing = await loadDiskStore();
    existing[key] = info;
    const keys = Object.keys(existing);
    if (keys.length > 500) {
      for (const old of keys.slice(0, keys.length - 500)) {
        delete existing[old];
      }
    }
    await mkdir(dirname(STORE_PATH), { recursive: true });
    await writeFile(STORE_PATH, JSON.stringify(existing, null, 2), "utf-8");
  } catch {
    // Non-fatal — in-memory cache still works
  }

  return key;
}

async function lookupThreadInfo(key: string): Promise<ThreadInfo | null> {
  const cached = threadCache.get(key);
  if (cached) return cached;
  try {
    const store = await loadDiskStore();
    const entry = store[key];
    if (entry) {
      threadCache.set(key, entry);
      return entry;
    }
  } catch {
    // ignore
  }
  return null;
}

// ---------------------------------------------------------------------------
// MIME type lookup (common types for email attachments)
// ---------------------------------------------------------------------------

const MIME_TYPES: Record<string, string> = {
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".gif": "image/gif",
  ".webp": "image/webp",
  ".svg": "image/svg+xml",
  ".bmp": "image/bmp",
  ".ico": "image/x-icon",
  ".pdf": "application/pdf",
  ".doc": "application/msword",
  ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  ".xls": "application/vnd.ms-excel",
  ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  ".ppt": "application/vnd.ms-powerpoint",
  ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
  ".zip": "application/zip",
  ".gz": "application/gzip",
  ".tar": "application/x-tar",
  ".json": "application/json",
  ".xml": "application/xml",
  ".csv": "text/csv",
  ".txt": "text/plain",
  ".md": "text/markdown",
  ".html": "text/html",
  ".css": "text/css",
  ".js": "text/javascript",
  ".ts": "text/typescript",
  ".py": "text/x-python",
  ".sh": "text/x-shellscript",
  ".mp3": "audio/mpeg",
  ".wav": "audio/wav",
  ".mp4": "video/mp4",
  ".webm": "video/webm",
  ".avi": "video/x-msvideo",
  ".mov": "video/quicktime",
};

function getMimeType(filePath: string): string {
  const ext = extname(filePath).toLowerCase();
  return MIME_TYPES[ext] || "application/octet-stream";
}

// ---------------------------------------------------------------------------
// File path extraction and attachment building
// ---------------------------------------------------------------------------

function extractFilePaths(text: string): string[] {
  // Match absolute paths under /home or /tmp only — these are the directories
  // where the agent saves output files. We intentionally exclude /etc, /root,
  // /usr, /var, /opt to avoid reading system files as attachments.
  const regex = /(?:^|[\s`(])(\/(home|tmp)[^\s`),;:!?'"<>*|]+\.[a-zA-Z0-9]{1,10})(?=[\s`),;:!?.'"<>]|$)/gm;
  const paths = new Set<string>();
  let match;
  while ((match = regex.exec(text)) !== null) {
    paths.add(match[1]);
  }
  return [...paths];
}

const MAX_SINGLE_ATTACHMENT_BYTES = 10 * 1024 * 1024; // 10MB per file
const MAX_TOTAL_ATTACHMENTS_BYTES = 10 * 1024 * 1024; // 10MB total

async function buildAttachments(
  filePaths: string[],
): Promise<Array<{ filename: string; content_type: string; data_base64: string }>> {
  const attachments: Array<{ filename: string; content_type: string; data_base64: string }> = [];
  let totalBytes = 0;

  for (const filePath of filePaths) {
    try {
      const resolved = await realpath(filePath);
      if (!resolved.startsWith("/home/") && !resolved.startsWith("/tmp/")) {
        console.warn(`[email-channel] Skipping attachment (outside allowed dirs): ${filePath} → ${resolved}`);
        continue;
      }
      await access(resolved, constants.R_OK);
      const data = await readFile(resolved);

      if (data.length > MAX_SINGLE_ATTACHMENT_BYTES) {
        console.warn(`[email-channel] Skipping attachment (>10MB): ${filePath}`);
        continue;
      }
      if (totalBytes + data.length > MAX_TOTAL_ATTACHMENTS_BYTES) {
        console.warn(`[email-channel] Skipping attachment (total >10MB): ${filePath}`);
        break;
      }

      totalBytes += data.length;
      attachments.push({
        filename: basename(filePath),
        content_type: getMimeType(filePath),
        data_base64: data.toString("base64"),
      });
    } catch {
      // File doesn't exist or not readable — skip silently
    }
  }

  return attachments;
}

// ---------------------------------------------------------------------------
// Channel meta + outbound adapter
// ---------------------------------------------------------------------------

const meta = {
  id: "email" as const,
  label: "Email",
  selectionLabel: "Email (genspark.email)",
  docsPath: "/channels/email",
  docsLabel: "email",
  blurb: "Send and receive emails via genspark.email.",
  aliases: ["mail"],
  order: 80,
};

type SendTextContext = {
  cfg: any;
  to: string;
  text: string;
  threadId?: string | number | null;
  replyToId?: string | null;
  accountId?: string | null;
  deps?: any;
  mediaUrl?: string;
  mediaLocalRoots?: readonly string[];
};

type OutboundResult = {
  channel: string;
  messageId: string;
  error?: string;
};

async function sendEmailViaBackend(ctx: SendTextContext): Promise<OutboundResult> {
  console.log(`[email-channel] sendEmailViaBackend: to=${ctx.to} textLen=${ctx.text?.length ?? 0} EMAIL_SEND_URL=${EMAIL_SEND_URL ? "SET" : "EMPTY"}`);

  const rawThreadId = ctx.threadId != null ? String(ctx.threadId) : "";

  if (!EMAIL_SEND_URL) {
    return { channel: "email", messageId: "", error: "OPENCLAW_EMAIL_SEND_URL not configured" };
  }

  // Decode thread info for proper email threading.
  // MessageThreadId is now a short hash key (to avoid ENAMETOOLONG in session
  // filenames). Look up the full subject + messageId from the thread store.
  // Falls back to JSON parse (legacy) and plain string (oldest format).
  let emailSubject = "Genspark Claw";
  let inReplyTo: string | undefined;

  const threadInfo = rawThreadId ? await lookupThreadInfo(rawThreadId) : null;

  // Suppress outbound for CC/BCC-only threads — the agent absorbed context
  // but should not reply to emails where it was merely CC'd or BCC'd.
  if (threadInfo?.ccOnly) {
    console.log(`[email-channel] Suppressing reply for CC-only thread: ${rawThreadId}`);
    return { channel: "email", messageId: "(cc-only-suppressed)" };
  }
  if (threadInfo) {
    const origSubject = threadInfo.subject || "Email";
    emailSubject = /^re:/i.test(origSubject) ? origSubject : `Re: ${origSubject}`;
    inReplyTo = threadInfo.messageId || undefined;
  } else {
    // Legacy fallback: try JSON parse (old format where MessageThreadId was raw JSON)
    try {
      const thread = JSON.parse(rawThreadId);
      const origSubject = thread.subject || "Email";
      emailSubject = /^re:/i.test(origSubject) ? origSubject : `Re: ${origSubject}`;
      inReplyTo = thread.messageId || undefined;
    } catch {
      // Oldest fallback: plain message-id string
      emailSubject = rawThreadId ? `Re: ${rawThreadId}` : "Genspark Claw";
      inReplyTo = rawThreadId || undefined;
    }
  }

  // Build reply body with quoted original (if available from thread store)
  let replyBody = ctx.text;
  if (threadInfo?.originalBody && threadInfo?.originalFrom) {
    const quotedLines = threadInfo.originalBody
      .split("\n")
      .map((line) => `> ${line}`)
      .join("\n");
    const dateStr = threadInfo.originalDate
      ? new Date(threadInfo.originalDate).toLocaleString("en-US", {
          dateStyle: "medium",
          timeStyle: "short",
        })
      : "";
    const attribution = dateStr
      ? `On ${dateStr}, ${threadInfo.originalFrom} wrote:`
      : `${threadInfo.originalFrom} wrote:`;
    replyBody = `${ctx.text}\n\n${attribution}\n${quotedLines}`;
  }

  const filePaths = extractFilePaths(ctx.text);
  const attachments = filePaths.length > 0 ? await buildAttachments(filePaths) : [];

  try {
    const resp = await fetch(EMAIL_SEND_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Email-Secret": EMAIL_SECRET,
      },
      body: JSON.stringify({
        vm_name: VM_NAME,
        email_address: EMAIL_ADDRESS,
        to_email: ctx.to,
        subject: emailSubject,
        body: replyBody,
        in_reply_to: ctx.replyToId || inReplyTo || undefined,
        attachments: attachments.length > 0 ? attachments : undefined,
      }),
    });

    if (!resp.ok) {
      const errText = await resp.text();
      console.error(`[email-channel] Backend send failed: ${resp.status} ${errText}`);
      return { channel: "email", messageId: "", error: errText };
    }

    const data = (await resp.json()) as { message_id?: string };
    return { channel: "email", messageId: data.message_id || "" };
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    console.error(`[email-channel] Send error: ${msg}`);
    return { channel: "email", messageId: "", error: msg };
  }
}

const outbound = {
  deliveryMode: "direct" as const,
  textChunkLimit: 50_000, // emails can be long

  async sendText(ctx: SendTextContext): Promise<OutboundResult> {
    return sendEmailViaBackend(ctx);
  },

  async sendMedia(ctx: SendTextContext): Promise<OutboundResult> {
    if (ctx.mediaUrl) {
      const textWithMedia = ctx.text
        ? `${ctx.text}\n\n[Attachment: ${ctx.mediaUrl}]`
        : `[Attachment: ${ctx.mediaUrl}]`;
      return sendEmailViaBackend({ ...ctx, text: textWithMedia });
    }
    return sendEmailViaBackend(ctx);
  },

  async sendPayload(ctx: any): Promise<OutboundResult> {
    const text = ctx.payload?.text ?? "";
    const mediaUrl = ctx.payload?.mediaUrl ?? ctx.payload?.mediaUrls?.[0] ?? "";
    return sendEmailViaBackend({ ...ctx, text, mediaUrl });
  },
};

const emailPlugin = {
  id: "email" as const,
  meta,

  capabilities: {
    chatTypes: ["direct"] as const,
    polls: false,
    threads: true, // email threading via Message-ID / In-Reply-To
    media: false,
    reactions: false,
    edit: false,
    reply: true,
  },

  config: {
    listAccountIds: (_cfg: any) => ["default"],
    resolveAccount: (_cfg: any, _accountId?: string) => ({
      accountId: "default",
      emailAddress: EMAIL_ADDRESS,
      vmName: VM_NAME,
    }),
  },

  gateway: {
    // The gateway tracks each channel/account's lifecycle via the
    // ``startAccount`` promise — its in-flight state is what populates
    // ``manifestRuntime`` and what the health-monitor reads to decide
    // whether the channel is "running" vs "stopped". Without this hook,
    // the channel never enters the running state, and health-monitor
    // restarts it on every cycle (``reason: stopped`` loop).
    //
    // Email is stateless: the inbound HTTP server is started once in
    // register() and outbound calls are direct fetches, so there is no
    // long-lived transport to keep alive here. Park on abortSignal to
    // hold the running state until the gateway tears the account down.
    startAccount: async (ctx: any) => {
      const accountId = ctx.accountId || "default";
      ctx.log?.info?.(`[email-channel] Starting account: ${accountId}`);
      // Guard against a missing abortSignal — without it the parking
      // promise below would never resolve and the channel would be stuck
      // "running" forever, with no way for the gateway to tear it down.
      // OpenClaw's gateway always passes abortSignal in current versions,
      // but this is the lifecycle's only exit, so we fail closed.
      const signal: AbortSignal | undefined = ctx.abortSignal;
      if (!signal) {
        ctx.log?.warn?.(`[email-channel] startAccount called without abortSignal; returning immediately so the gateway can re-call when ready`);
        return;
      }
      await new Promise<void>((resolve) => {
        if (signal.aborted) return resolve();
        signal.addEventListener("abort", () => resolve(), { once: true });
      });
      ctx.log?.info?.(`[email-channel] Stopping account: ${accountId}`);
    },
  },

  outbound,
};

// ---------------------------------------------------------------------------
// Inbound HTTP server (POST /api/email/inbound on port 18793)
// ---------------------------------------------------------------------------

type InboundPayload = {
  from: string;
  to: string;
  subject: string;
  body: string;
  message_id: string;
  session_key: string;
  to_header?: string; // Full To header (all recipients)
  cc?: string;
  bcc?: string;
  date?: string;
  cc_only?: boolean; // VM email in Cc only (not in To) — absorb context, don't reply
  attachments?: Array<{ filename: string; content_type: string; url: string }>;
};

function readBody(req: IncomingMessage): Promise<string> {
  return new Promise((resolve, reject) => {
    const chunks: Buffer[] = [];
    req.on("data", (chunk: Buffer) => chunks.push(chunk));
    req.on("end", () => resolve(Buffer.concat(chunks).toString("utf-8")));
    req.on("error", reject);
  });
}

function respond(res: ServerResponse, status: number, body: Record<string, unknown>) {
  res.writeHead(status, { "Content-Type": "application/json" });
  res.end(JSON.stringify(body));
}

let inboundServerStarted = false;
let currentApi: any = null;

function startEmailInboundServer(port: number, api: any): void {
  currentApi = api;

  const server = createServer(async (req: IncomingMessage, res: ServerResponse) => {
    const _api = currentApi;
    if (req.url !== "/api/email/inbound" && req.url !== "/api/email/inbound/") {
      respond(res, 404, { error: "Not found" });
      return;
    }

    if (req.method !== "POST") {
      respond(res, 405, { error: "Method not allowed" });
      return;
    }

    const secret = req.headers["x-email-secret"] as string | undefined;
    if (!EMAIL_SECRET) {
      respond(res, 500, { error: "OPENCLAW_EMAIL_SECRET not configured" });
      return;
    }
    if (secret !== EMAIL_SECRET) {
      respond(res, 403, { error: "Invalid secret" });
      return;
    }

    let payload: InboundPayload;
    try {
      const raw = await readBody(req);
      payload = JSON.parse(raw);
    } catch {
      respond(res, 400, { error: "Invalid JSON" });
      return;
    }

    const { from, subject, body, message_id, session_key } = payload;
    if (!from || !body) {
      respond(res, 400, { error: "Missing required fields: from, body" });
      return;
    }

    // Respond immediately, dispatch asynchronously.
    respond(res, 200, { status: "accepted" });

    dispatchEmailToAgent({
      from,
      subject: subject || "(no subject)",
      body,
      messageId: message_id || "",
      sessionKey: session_key || "main",
      toHeader: payload.to_header || "",
      cc: payload.cc || "",
      bcc: payload.bcc || "",
      date: payload.date || "",
      ccOnly: payload.cc_only || false,
      attachments: payload.attachments,
      logger: _api.logger,
    }).catch((err) => {
      const msg = err instanceof Error ? err.message : String(err);
      _api.logger.error(`[email-channel] Inbound dispatch error: ${msg}`);
    });
  });

  // Retry on EADDRINUSE — `openclaw plugins install` briefly loads the plugin
  // and binds this port; if the install process hasn't exited yet when the
  // gateway starts, the port is still held.
  const MAX_RETRIES = 5;
  const RETRY_DELAY_MS = 2000;
  let attempt = 0;

  const tryListen = () => {
    server.listen(port, "127.0.0.1", () => {
      currentApi.logger.info(`[email-channel] Inbound HTTP server listening on 127.0.0.1:${port} (POST /api/email/inbound)`);
    });
  };

  // unref() so that `openclaw plugins install` (which runs the plugin briefly to
  // register it) can exit after installation without being held open by this server.
  server.unref();

  server.on("error", (err: NodeJS.ErrnoException) => {
    if (err.code === "EADDRINUSE" && attempt < MAX_RETRIES) {
      attempt++;
      currentApi.logger.warn(
        `[email-channel] Port ${port} in use, retrying in ${RETRY_DELAY_MS}ms (attempt ${attempt}/${MAX_RETRIES})`,
      );
      setTimeout(tryListen, RETRY_DELAY_MS);
    } else {
      currentApi.logger.error(`[email-channel] Inbound server error: ${err.message}`);
    }
  });

  tryListen();
}

/**
 * Dispatch an inbound email to the agent using the OpenClaw plugin runtime.
 *
 * Follows the same pattern as genspark-im's handleMessage:
 * 1. Build MsgContext via finalizeInboundContext()
 * 2. Record inbound session metadata
 * 3. Dispatch via dispatchReplyWithBufferedBlockDispatcher with a deliver
 *    callback that calls emailPlugin.outbound.sendText() directly.
 *
 * We do NOT use withReplyDispatcher + dispatchReplyFromConfig because
 * routeReply("email") silently fails — "email" is not in OpenClaw's built-in
 * CHAT_CHANNEL_ORDER and isRoutableChannel("email") returns false.
 */
async function dispatchEmailToAgent(params: {
  from: string;
  subject: string;
  body: string;
  messageId: string;
  sessionKey: string;
  toHeader: string;
  cc: string;
  bcc: string;
  date: string;
  ccOnly: boolean;
  attachments?: Array<{ filename: string; content_type: string; url: string }>;
  logger: any;
}): Promise<void> {
  const core = getEmailRuntime();
  const cfg = core.config?.loadConfig?.();

  if (!cfg) {
    throw new Error("OpenClaw config not available (runtime.config.loadConfig failed)");
  }

  const { from, subject, body, messageId, sessionKey, toHeader, cc, bcc, date, ccOnly, attachments } = params;

  let messageBody = ccOnly
    ? `[Email CC'd to you — read and remember this conversation for context. Do NOT send any reply.]\nFrom: ${from}\nTo: ${toHeader || process.env.OPENCLAW_EMAIL_ADDRESS || ""}`
    : `[Email received]\nFrom: ${from}\nTo: ${toHeader || process.env.OPENCLAW_EMAIL_ADDRESS || ""}`;
  if (cc) {
    messageBody += `\nCc: ${cc}`;
  }
  if (bcc) {
    messageBody += `\nBcc: ${bcc}`;
  }
  messageBody += `\nSubject: ${subject}\n\n${body}`;

  const imageUrls: string[] = [];
  if (attachments && attachments.length > 0) {
    messageBody += "\n\nAttachments:";
    for (const att of attachments) {
      messageBody += `\n  - ${att.filename} (${att.content_type}): ${att.url}`;
      if (att.content_type.startsWith("image/")) {
        imageUrls.push(att.url);
      }
    }
  }

  const mediaPayload: Record<string, unknown> = {};
  if (imageUrls.length > 0) {
    mediaPayload.ImageUrl = imageUrls[0];
    mediaPayload.ImageUrls = imageUrls;
  }

  const ctx = core.channel.reply.finalizeInboundContext({
    Body: messageBody,
    BodyForAgent: messageBody,
    RawBody: body,
    CommandBody: messageBody,
    From: from,
    To: process.env.OPENCLAW_EMAIL_ADDRESS || "",
    SessionKey: sessionKey,
    AccountId: "default",
    ChatType: "direct",
    SenderName: from,
    SenderId: from,
    Provider: "email",
    Surface: "email",
    MessageSid: messageId,
    Timestamp: Date.now(),
    WasMentioned: true,
    CommandAuthorized: true,
    OriginatingChannel: "email",
    OriginatingTo: from,
    MessageThreadId: await storeThreadInfo(subject, messageId, {
      originalBody: body,
      originalFrom: from,
      originalDate: date || new Date().toISOString(),
      ccOnly: ccOnly || undefined,
    }),
    ...mediaPayload,
  });

  params.logger.info(
    `[email-channel] Dispatching email: from=${from} subject=${subject} session=${sessionKey} ccOnly=${ccOnly}`,
  );

  try {
    const storePath = core.channel.session.resolveStorePath(cfg?.session?.store, {
      agentId: cfg?.agent?.id || "default",
    });
    await core.channel.session.recordInboundSession({
      storePath,
      sessionKey,
      ctx,
      onRecordError: (err: Error) => {
        params.logger.warn(`[email-channel] recordInboundSession meta error: ${err}`);
      },
    });
  } catch (e) {
    params.logger.warn(`[email-channel] recordInboundSession failed: ${e}`);
  }

  await core.channel.reply.dispatchReplyWithBufferedBlockDispatcher({
    ctx,
    cfg,
    dispatcherOptions: {
      deliver: async (payload: any, info: any) => {
        const text = payload?.text;
        if (!text) return;
        params.logger.info(
          `[email-channel] Delivering ${info?.kind || "reply"} (${text.length} chars) to ${from}`,
        );
        try {
          await emailPlugin.outbound.sendText({
            to: from,
            text,
            threadId: ctx.MessageThreadId,
            cfg,
          });
        } catch (e) {
          const msg = e instanceof Error ? e.message : String(e);
          params.logger.error(`[email-channel] deliver failed: ${msg}`);
        }
      },
      onError: (err: any, info: any) => {
        params.logger.error(`[email-channel] Dispatch error (${info?.kind}): ${err}`);
      },
    },
  });

  params.logger.info(`[email-channel] Email dispatched to agent: session=${sessionKey}`);
}

// ---------------------------------------------------------------------------
// Plugin entry point
// ---------------------------------------------------------------------------

const plugin = {
  id: "genspark-email",
  name: "Genspark Email Channel",
  description: "Email channel for OpenClaw via genspark.email / MailChannels",
  configSchema: { type: "object" as const, properties: {} },
  register(api: any) {
    setEmailRuntime(api.runtime);
    api.registerChannel({ plugin: emailPlugin });
    // Guard against multiple register() calls — gateway may invoke this
    // more than once (e.g. plugin reload, config hot-swap). Only the first
    // call should bind the inbound HTTP server to avoid EADDRINUSE errors.
    // Also skip during `openclaw plugins install` — the install process loads
    // the plugin briefly to extract metadata, but the inbound server should
    // only run in the gateway process.
    if (!inboundServerStarted && !process.env.OPENCLAW_PLUGIN_INSTALL_ONLY) {
      inboundServerStarted = true;
      startEmailInboundServer(18793, api);
    } else {
      currentApi = api;
    }
    api.logger.info("[email-channel] Email channel plugin registered");
  },
};

export default plugin;

