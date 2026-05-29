#!/usr/bin/env bash
set -euo pipefail

QUEUE_DIR="${QUEUE_DIR:-/opt/genspark-claw/queue/local}"
RUN_DIR="${RUN_DIR:-/opt/genspark-claw/run/local}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "${QUEUE_DIR}" "${RUN_DIR}"

shopt -s nullglob
for job in "${QUEUE_DIR}"/*.json; do
  out="$("${SCRIPT_DIR}/call_local_worker.sh" "${job}")" || true
  if [[ -f "${out}" ]]; then
    rm -f "${job}"
  fi
done
