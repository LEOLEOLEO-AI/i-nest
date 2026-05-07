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
 */

import { emailPlugin } from "./src/channel.js";
import { startEmailInboundServer, updateInboundApi } from "./src/inbound.js";
import { setEmailRuntime } from "./src/runtime.js";

let inboundServerStarted = false;

const plugin = {
  id: "genspark-email",
  name: "Genspark Email Channel",
  description: "Email channel for OpenClaw via genspark.email / MailChannels",
  configSchema: { type: "object" as const, properties: {} },
  register(api: any) {
    setEmailRuntime(api.runtime);
    api.registerChannel({ plugin: emailPlugin });
    // Guard against multiple register() calls — gateway may invoke this
    // more than once (e.g. plugin reload, config hot-swap).  Only the first
    // call should bind the inbound HTTP server to avoid EADDRINUSE errors.
    // Also skip during `openclaw plugins install` — the install process loads
    // the plugin briefly to extract metadata, but the inbound server should
    // only run in the gateway process.  The configure script sets
    // OPENCLAW_PLUGIN_INSTALL_ONLY=1 during plugin installation.
    if (!inboundServerStarted && !process.env.OPENCLAW_PLUGIN_INSTALL_ONLY) {
      inboundServerStarted = true;
      startEmailInboundServer(18793, api);
    } else {
      // Update the api reference so the running server uses the latest logger
      updateInboundApi(api);
    }
    api.logger.info("[email-channel] Email channel plugin registered");
  },
};

export default plugin;

