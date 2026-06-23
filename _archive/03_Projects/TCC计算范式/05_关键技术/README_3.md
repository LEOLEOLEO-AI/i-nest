# Genspark Claw → Local Worker Bridge

This folder contains scripts that let a remote Linux host enqueue jobs and execute them on this Windows machine via SSH reverse tunnel.

## Local (Windows)

1. Enable OpenSSH server:
   - Run `setup_windows_openssh.ps1` as Administrator.
2. Start a reverse tunnel to the cloud host:
   - Run `start_reverse_tunnel.ps1 -CloudHost <host> -CloudUser <user>`
3. Local job runner:
   - `local_worker.ps1` reads a JSON job file and runs predefined maintenance tasks (wiki generation, health checks, git sync).

## Cloud (Linux)

Use the scripts in `cloud/` to:
- enqueue jobs when local is offline
- dispatch jobs to local through the reverse tunnel (cloud -> localhost:2222)
- pull back `result.json` and artifacts paths

## Security

Avoid embedding passwords/tokens into URLs or scripts. Use SSH keys or credential manager.
