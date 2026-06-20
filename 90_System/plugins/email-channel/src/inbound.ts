/**
 * HTTP route: POST /api/email/inbound
 *
 * Receives inbound emails from the Genspark backend, builds MsgContext
 * with OriginatingChannel="email", and dispatches to the agent using
 * the proper OpenClaw plugin runtime API (same as Feishu/Slack/Telegram).
 *
 * Auth: X-Email-Secret header (per-VM secret).
 */

import { createServer } from "http";
import type { IncomingMessage, ServerResponse } from "http";
import { emailPlugin } from "./channel.js";
import { getEmailRuntime } from "./runtime.js";
import { storeThreadInfo } from "./thread-store.js";

const EMAIL_SECRET = process.env.OPENCLAW_EMAIL_SECRET || "";

type InboundPayload = {
  from: string;
  to: string;
  subject: string;
  body: string;
  message_id: string;
  session_key: string;
  to_header?: string; // Full To header (all recipients)
  cc?: string; // Cc header
  bcc?: string; // Bcc header (rarely present — stripped by most MTAs)
  date?: string; // Original email Date header
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

/**
 * Start an independent HTTP server for POST /api/email/inbound.
 *
 * Uses its own http.createServer() on a dedicated port instead of
 * api.registerHttpRoute(), which avoids the OpenClaw 3.22 gateway
 * plugin-route registry bug (routes registered dynamically are invisible
 * to the HTTP handler's startup-time snapshot).  This pattern is also
 * used by the Feishu and Telegram channel plugins.
 *
 * Caddy reverse-proxies external /api/email/inbound requests to this port.
 */
// Mutable api reference — updated on each register() call so the running
// server always uses the latest logger even after plugin hot-reloads.
let currentApi: any = null;

export function updateInboundApi(api: any): void {
  currentApi = api;
}

export function startEmailInboundServer(port: number, api: any): void {
  currentApi = api;

  const server = createServer(async (req: IncomingMessage, res: ServerResponse) => {
    const _api = currentApi;
    // Only handle /api/email/inbound — return 404 for any other path
    if (req.url !== "/api/email/inbound" && req.url !== "/api/email/inbound/") {
      respond(res, 404, { error: "Not found" });
      return;
    }

    if (req.method !== "POST") {
      respond(res, 405, { error: "Method not allowed" });
      return;
    }

    // Verify per-VM email secret
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
    // Agent processing can take 10-60s; don't block the HTTP response.
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
  // gateway starts, the port is still held.  Retry a few times with backoff
  // instead of failing permanently.
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
  // The gateway process itself is kept alive by its own handles, so the server
  // remains active during normal operation.
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

  // Build the message text that the agent sees.
  // Include To/Cc/Bcc so the agent knows if it was a direct recipient or CC'd.
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

  // Append attachment info to the message
  const imageUrls: string[] = [];
  if (attachments && attachments.length > 0) {
    messageBody += "\n\nAttachments:";
    for (const att of attachments) {
      messageBody += `\n  - ${att.filename} (${att.content_type}): ${att.url}`;
      // Collect image URLs for vision model support
      if (att.content_type.startsWith("image/")) {
        imageUrls.push(att.url);
      }
    }
  }

  // Build media payload for vision-capable models
  const mediaPayload: Record<string, unknown> = {};
  if (imageUrls.length > 0) {
    mediaPayload.ImageUrl = imageUrls[0];
    mediaPayload.ImageUrls = imageUrls;
  }

  // Build MsgContext with email routing info
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
    // Use a short hash key as MessageThreadId to avoid ENAMETOOLONG errors.
    // OpenClaw uses this value in session filenames — URL-encoded Chinese
    // subjects + long Outlook Message-IDs can exceed the 255-byte limit.
    // The outbound handler looks up the hash to recover the original
    // subject (for "Re: ..." line) and messageId (for In-Reply-To header).
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

  // Record inbound session metadata (best-effort — don't let errors abort delivery)
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

  // Dispatch to agent. Reply delivery is via the deliver callback which calls
  // emailPlugin.outbound.sendText() directly — bypassing routeReply() which
  // does not support plugin-registered channels ("email" is not in CHAT_CHANNEL_ORDER).
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

