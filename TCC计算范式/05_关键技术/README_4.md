# Cloud side setup

1. Copy this folder to the cloud host (example target: `/tmp/trae_bridge_cloud/`).
2. Run as root:
   - `bash /tmp/trae_bridge_cloud/install_cloud_bridge.sh`
3. Set environment variables for dispatch:
   - `LOCAL_USER` (Windows username used for SSH)
   - `LOCAL_PORT=2222`
4. Enqueue and dispatch a job:
   - `echo '{"task":"wiki_update","args":{}}' > /tmp/job.json`
   - `/opt/genspark-claw/scripts/call_local_worker.sh /tmp/job.json`
