#!/usr/bin/env bash
set -euo pipefail

JOB_FILE="${1:-}"
if [[ -z "${JOB_FILE}" ]]; then
  echo "usage: call_local_worker.sh <job.json>" >&2
  exit 2
fi

LOCAL_PORT="${LOCAL_PORT:-2222}"
LOCAL_USER="${LOCAL_USER:-$USER}"
LOCAL_HOST="${LOCAL_HOST:-127.0.0.1}"

QUEUE_DIR="${QUEUE_DIR:-/opt/genspark-claw/queue/local}"
RUN_DIR="${RUN_DIR:-/opt/genspark-claw/run/local}"

mkdir -p "${QUEUE_DIR}" "${RUN_DIR}"

job_id="$(date +%Y%m%d_%H%M%S)_$RANDOM"
queued_job="${QUEUE_DIR}/${job_id}.json"
cp "${JOB_FILE}" "${queued_job}"

ssh_opts=(
  -p "${LOCAL_PORT}"
  -o ConnectTimeout=5
  -o BatchMode=yes
  -o StrictHostKeyChecking=accept-new
)

if ! ssh "${ssh_opts[@]}" "${LOCAL_USER}@${LOCAL_HOST}" "exit 0" >/dev/null 2>&1; then
  echo "${queued_job}"
  exit 0
fi

remote_dir="claw_jobs/${job_id}"
ssh "${ssh_opts[@]}" "${LOCAL_USER}@${LOCAL_HOST}" "mkdir -p ${remote_dir}"
scp -P "${LOCAL_PORT}" "${queued_job}" "${LOCAL_USER}@${LOCAL_HOST}:${remote_dir}/job.json" >/dev/null

remote_cmd="powershell -NoProfile -ExecutionPolicy Bypass -File ${remote_dir}/local_worker.ps1 -JobFile ${remote_dir}/job.json"

scp -P "${LOCAL_PORT}" "$(dirname "$0")/../local_worker.ps1" "${LOCAL_USER}@${LOCAL_HOST}:${remote_dir}/local_worker.ps1" >/dev/null

result_path="$(ssh "${ssh_opts[@]}" "${LOCAL_USER}@${LOCAL_HOST}" "${remote_cmd}")"
local_result="${RUN_DIR}/${job_id}_result.json"
scp -P "${LOCAL_PORT}" "${LOCAL_USER}@${LOCAL_HOST}:${result_path}" "${local_result}" >/dev/null

echo "${local_result}"
