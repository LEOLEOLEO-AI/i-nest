/**
 * Email channel plugin definition.
 *
 * Implements the ChannelPlugin contract with a minimal outbound adapter
 * that POSTs agent replies to the Genspark backend for delivery via
 * MailChannels.
 *
 * Config is read from environment variables injected during VM configure:
 *   OPENCLAW_EMAIL_SEND_URL    — backend endpoint for outbound email
 *   OPENCLAW_EMAIL_SECRET       — per-VM secret for auth
 *   OPENCLAW_EMAIL_ADDRESS     — this VM's email address (e.g. vm-name@genspark.email)
 *   OPENCLAW_VM_NAME           — VM name for identifying the sender
 */

import { readFile, access, realpath } from "fs/promises";
import { basename, extname } from "path";
import { constants } from "fs";
import { lookupThreadInfo } from "./thread-store.js";

// ---------------------------------------------------------------------------
// Config from environment
// ---------------------------------------------------------------------------

const EMAIL_SEND_URL = process.env.OPENCLAW_EMAIL_SEND_URL || "";
const EMAIL_SECRET = process.env.OPENCLAW_EMAIL_SECRET || "";
const EMAIL_ADDRESS = process.env.OPENCLAW_EMAIL_ADDRESS || "";
const VM_NAME = process.env.OPENCLAW_VM_NAME || "";

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

/** Extract absolute file paths from text (e.g. `/home/work/.openclaw/workspace/output.png`) */
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

/** Read files from disk and build base64-encoded attachment payloads */
async function buildAttachments(
  filePaths: string[],
): Promise<Array<{ filename: string; content_type: string; data_base64: string }>> {
  const attachments: Array<{ filename: string; content_type: string; data_base64: string }> = [];
  let totalBytes = 0;

  for (const filePath of filePaths) {
    try {
      // Resolve symlinks and ".." to get the real path, then verify it
      // stays under /home or /tmp to prevent path traversal attacks.
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
// Channel meta
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

// ---------------------------------------------------------------------------
// Outbound adapter — delivers agent replies via backend HTTP endpoint
// ---------------------------------------------------------------------------

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

  // Try hash-based lookup first (new format)
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

  // Extract file paths from the reply text and build attachments
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
    // Deliver media as text (URL) for now; future: attach as inline image
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

// ---------------------------------------------------------------------------
// Channel plugin export
// ---------------------------------------------------------------------------

export const emailPlugin = {
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

  outbound,
};

