#!/bin/bash
# Shared Chromium command definition — sourced by start-vnc.sh and start-browser.sh
# Single source of truth for Chromium flags (CDP port, profile dir, etc.)
CHROMIUM_CMD="chromium-browser \
--user-data-dir=/home/work/.chromium-profile \
--remote-debugging-port=9222 \
--remote-debugging-address=127.0.0.1 \
--no-sandbox --disable-gpu --disable-dev-shm-usage \
--no-first-run --disable-default-apps \
--no-restore-session-state --disable-session-crashed-bubble"

