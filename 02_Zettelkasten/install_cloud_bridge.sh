#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="${TARGET_DIR:-/opt/genspark-claw/scripts}"
SYSTEMD_DIR="${SYSTEMD_DIR:-/etc/systemd/system}"

mkdir -p "${TARGET_DIR}"

cp "$(dirname "$0")/call_local_worker.sh" "${TARGET_DIR}/call_local_worker.sh"
cp "$(dirname "$0")/process_queue.sh" "${TARGET_DIR}/process_queue.sh"

chmod +x "${TARGET_DIR}/call_local_worker.sh" "${TARGET_DIR}/process_queue.sh"

cp "$(dirname "$0")/local-worker-queue.service" "${SYSTEMD_DIR}/local-worker-queue.service"
cp "$(dirname "$0")/local-worker-queue.timer" "${SYSTEMD_DIR}/local-worker-queue.timer"

systemctl daemon-reload
systemctl enable --now local-worker-queue.timer

systemctl status local-worker-queue.timer --no-pager
