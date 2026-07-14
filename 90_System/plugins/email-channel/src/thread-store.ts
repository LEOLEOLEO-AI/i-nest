/**
 * Persistent store for email thread metadata (subject + messageId).
 *
 * Problem: OpenClaw uses MessageThreadId as part of the session filename.
 * When MessageThreadId contains URL-encoded Chinese subjects and long
 * Outlook Message-IDs, the filename exceeds Linux's 255-byte limit
 * (ENAMETOOLONG).
 *
 * Solution: Use a short hash as the MessageThreadId and store the full
 * thread info (subject + messageId) in a JSON file on disk. The outbound
 * handler looks up the hash to reconstruct email headers.
 */

import { createHash } from "crypto";
import { readFile, writeFile, mkdir } from "fs/promises";
import { dirname } from "path";

export type ThreadInfo = {
  subject: string;
  messageId: string;
  /** Original email body for quoting in replies */
  originalBody?: string;
  /** Sender of the original email (for attribution in quote) */
  originalFrom?: string;
  /** Timestamp of the original email */
  originalDate?: string;
  /** VM was CC'd/BCC'd only (not in To) — absorb context, suppress reply */
  ccOnly?: boolean;
};

// In-memory cache (fast lookups within the same Gateway process lifetime)
const cache = new Map<string, ThreadInfo>();

// Disk path — co-located with session files
const STORE_DIR = process.env.OPENCLAW_DATA_DIR || "/home/work/.openclaw";
const STORE_PATH = `${STORE_DIR}/agents/main/email-thread-info.json`;

/**
 * Generate a short, filesystem-safe hash key from thread info.
 * 12 hex chars = 48 bits of entropy — collision-safe for email volumes.
 */
export function threadKey(subject: string, messageId: string): string {
  const input = JSON.stringify({ subject, messageId });
  return createHash("sha256").update(input).digest("hex").slice(0, 12);
}

/**
 * Store thread info and return the short hash key.
 */
export async function storeThreadInfo(
  subject: string,
  messageId: string,
  extra?: { originalBody?: string; originalFrom?: string; originalDate?: string; ccOnly?: boolean },
): Promise<string> {
  const key = threadKey(subject, messageId);
  const info: ThreadInfo = { subject, messageId, ...extra };
  cache.set(key, info);

  // Cap in-memory cache at 500 entries (same as disk store)
  if (cache.size > 500) {
    const iter = cache.keys();
    for (let i = cache.size - 500; i > 0; i--) {
      cache.delete(iter.next().value!);
    }
  }

  // Persist to disk (best-effort — cache is the primary source)
  try {
    const existing = await loadDiskStore();
    existing[key] = info;
    // Cap at 500 entries to prevent unbounded growth
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

/**
 * Look up thread info by hash key.
 */
export async function lookupThreadInfo(key: string): Promise<ThreadInfo | null> {
  // Try in-memory cache first
  const cached = cache.get(key);
  if (cached) return cached;

  // Fall back to disk
  try {
    const store = await loadDiskStore();
    const entry = store[key];
    if (entry) {
      cache.set(key, entry); // warm the cache
      return entry;
    }
  } catch {
    // ignore
  }

  return null;
}

async function loadDiskStore(): Promise<Record<string, ThreadInfo>> {
  try {
    const raw = await readFile(STORE_PATH, "utf-8");
    return JSON.parse(raw);
  } catch {
    return {};
  }
}

