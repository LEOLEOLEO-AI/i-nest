#!/bin/bash
# OpenClaw Browser — Chromium only (on-demand)
# Requires openclaw-vnc.service to be running (provides Xvfb :99 + Fluxbox)
# Deployed to ~/.openclaw/start-browser.sh by configure script
export DISPLAY=:99

# Kill any existing browser
pkill -f chromium 2>/dev/null
pkill -f chrome 2>/dev/null
sleep 1

# Shared Chromium flags (single source of truth)
source "$HOME/.openclaw/chromium-env.sh"

DISPLAY=:99 $CHROMIUM_CMD about:blank &
sleep 2

echo "Browser started (Chromium with CDP on :9222)"

