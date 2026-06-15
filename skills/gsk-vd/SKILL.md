---
name: gsk-vd
version: 1.0.0
description: "Virtual Developer — drive a VD project (issues, VMs, templates, shell exec, GitHub) from the CLI / local OpenCode. Gated behind gk_vd_project_agent and requires vd_project_id to be configured."
metadata:
  category: virtual-developer
  requires:
    bins:
      - gsk
  cliHelp: gsk vd --help
---

# gsk-vd — Virtual Developer CLI

**PREREQUISITE:** Read `../gsk-shared/SKILL.md` first for auth, global flags, and output conventions.

`gsk vd <subcmd>` drives an existing Virtual Developer project end-to-end from a shell. It exposes the exact same 21 tools the Web UI's `VdProjectAgentChat` agent uses (`backend/virtual_developer/project_agent/agent.py`) — issue CRUD + dispatch, VM lifecycle (start/stop/create/delete/save_snapshot), on-VM shell exec, OpenCode session inspection, GitHub App auth, and VM template management.

Use this skill when you are **driving** an already-provisioned VD project as a CI-like agent (creating issues, dispatching work to VMs, inspecting PRs, running shell commands on the VM). **Do not** use it to create the VD project itself — that stays in the web UI.

## Activation

`gsk vd` is hidden by default. It becomes available only when **both** conditions hold:

1. **Server-side:** the user has the `gk_vd_project_agent` gatekeeper flag (closed beta).
2. **Client-side:** a `vd_project_id` is configured — either in the gsk config file or via `GSK_VD_PROJECT_ID` env.

### Enable via config file

Add to `~/.genspark-tool-cli/config.json`:

```json
{
  "api_key": "gsk-...",
  "base_url": "http://localhost:8582",
  "vd_project_id": "vd-proj-abc123"
}
```

### Enable via env var

```bash
export GSK_VD_PROJECT_ID=vd-proj-abc123
```

### Use an alternate config profile

If you want to keep your default profile untouched (e.g. to drive a dev-backend VD project from the same machine that talks to prod for other gsk commands):

```bash
# Point gsk at a separate config file — also affects where tools-cache.json lives
export GSK_CONFIG=/path/to/vd-profile/config.json
# or per-command
gsk --config /path/to/vd-profile/config.json vd list_vms
```

Once activated, every `gsk vd <subcmd>` command auto-injects the resolved `vd_project_id` as the default for its `--vd_project_id` flag. You can still override per-call with `--vd_project_id <other-id>`.

## Conventions

- All 21 commands accept `--vd_project_id <id>` but it is auto-defaulted from config; you rarely need to pass it.
- All commands return an NDJSON response with `{version, status, message, data, session_state}`. Tool-specific payload is under `data`.
- A tool that fails business-layer validation (wrong state, missing permission, not found) returns `status: "error"` with a human-readable `message`; this is **not** an infra error — inspect and retry with adjusted args.
- Long-running operations (template snapshot, VM provisioning) return immediately with a `"creating" | "provisioning"` status. Poll via the corresponding Get / List tool until the status changes.

## Tool catalog

### Project & issues

| Subcommand | Required flags | Purpose |
|---|---|---|
| `gsk vd get_project_overview` | — | Returns project metadata, repos, VMs (id + ready_state), and an `issues_summary` bucket count. Your first call in any workflow. |
| `gsk vd list_issues` | `[--status <state>]` | List issues. Without `--status` you get all; with it, filter to one of: `pending`, `working`, `wait_human`, `waiting_code_review`, `testing`, `pending_user_confirm`, `completed`, `failed`, `cancelled`. |
| `gsk vd get_issue_detail` | `--issue_id <id>` | Full issue record incl. `status`, `pr_url`, `assigned_vm_id`, `work_log` (state transitions with timestamps), `test_result`, `attempt_count`. |
| `gsk vd issue_action` | `--issue_id <id> --action <verb>` | Move an issue through its lifecycle. `action` ∈ `continue`, `cancel`, `run_tests`, `confirm_merge`, `reject_merge`, `submit_review`, `retry`. `--reason` is optional text recorded in the work log. |
| `gsk vd create_github_issue` | `--repo_id <id> --title <t> --body <md>` | Creates a new GitHub issue in the project's repo. The webhook handler will mirror it back as a VD issue shortly. Use after `get_project_overview` to read the `repo_id`. |
| `gsk vd dispatch_issues` | — | One-shot scheduler trigger: pops the oldest `pending` issue and assigns it to the first idle VM. Returns `assigned: [{issue_id, vm_id}]`. Useful when you want to "push" without waiting for the periodic scheduler. |

### VMs

| Subcommand | Required flags | Purpose |
|---|---|---|
| `gsk vd list_vms` | — | List all VMs in the project with id, vm_name, ready_state, current_issue_id, public preview_url / domain. |
| `gsk vd get_vm_status` | `--vm_id <id>` | Same fields as `list_vms` but single VM, plus public_ip. |
| `gsk vd vm_action` | `--vm_id <id> --action <start\|stop>` | Start or stop a VM. These are synchronous (~10-60s). **Note:** other lifecycle actions (suspend/resume/save_snapshot/reset) are not exposed via this minimal wrapper — use the Web UI or direct API for those. |
| `gsk vd create_vm` | — | Provision a new VM with project defaults. `--vm_size <lite\|standard\|high>` picks the tier (default `standard`): `lite` = 2C/4G Standard_B2s (64GB), `standard` = 2C/8G Standard_B2ms (64GB), `high` = 4C/16G Standard_B4ms (128GB). Returns immediately with `vm_id` + `status: "provisioning"`. Poll `get_vm_status` until `ready_state == "ready"` (~3-5 min). |
| `gsk vd delete_vm` | `--vm_id <id>` | Delete a VM (soft delete; underlying Azure instance is also deleted). Confirm with user before calling. |
| `gsk vd update_vm_startup_script` | `--vm_id <id> --startup_script <shell>` | Overwrite the VM's `startup_script` field. Typically a `#!/bin/bash` script that attaches to a tmux session on SSH login. |
| `gsk vd reconfigure_vm` | `--vm_id <id>` | Re-run the full VM env setup: apt packages, opencode install, VS Code Remote profile, Caddy `:8443` reverse proxy, user SSH key, gsk token. **Use when a VM provisioned before a given config step existed is missing something** — e.g. preview URL at `:8443` returns CORS errors because Caddy was never configured. Idempotent. VM must be `ready` or `working`. Takes ~30-60s; briefly interrupts the preview URL during Caddy restart. Returns per-step status (`ok`/`failed`/`skipped`) for user-key and gsk-token injection. |
| `gsk vd resize_vm` | `--vm_id <id> --vm_size <lite\|standard\|high>` | Resize a VM to a different tier. VM must be `ready` or `suspended`. Runs deallocate → Azure SKU change → optional disk grow → start (if it was running). Takes ~60-120s. **Disk can only grow, not shrink** — down-resize keeps the existing disk size. |

### Exec / sessions

| Subcommand | Required flags | Purpose |
|---|---|---|
| `gsk vd execute_command` | `--vm_id <id> --command <sh>` | Run a shell command on the VM via SSH. `--timeout <sec>` (default 30, max 120). Returns `{exit_code, stdout, stderr}`. VM must be `ready` (not `suspended`). |
| `gsk vd get_session_messages` | `--vm_id <id> [--session_id <sid>]` | Without `--session_id`: list OpenCode sessions on that VM. With it: fetch message transcript. |
| `gsk vd get_pr_info` | `--issue_id <id> [--include_diff]` | Fetch GitHub PR metadata (title, state, mergeable, review comments). `--include_diff` returns full diff (can be large). Issue must be past PR-creation phase. |

### GitHub integration

| Subcommand | Required flags | Purpose |
|---|---|---|
| `gsk vd check_github_auth` | `--repo_id <id>` | Verify the VD GitHub App installation for this repo can still acquire an installation token. Returns `ok`, `repo_full_name`, `installation_id`, `expires_at`. Use this when a VM reports 401s from git/GitHub API. |
| `gsk vd refresh_vm_github_token` | `--vm_id <id> --repo_id <id>` | Re-issue a fresh installation token and inject it into the VM's `~/.netrc` / git credential helper. Run this if `check_github_auth` succeeds but the VM still sees auth errors (token expired inside VM). |
| `gsk vd get_repo_github_token` | `--repo_id <id>` | Issue a GitHub App installation token and **return it to the caller** (not a VM) so local `gh` / `git` can act on the repo — merge PRs, push, clone from your laptop. Token inherits the App's installed permissions (repo read+write) and expires in ~1h (GitHub API cap); re-call for a fresh one. **WARNING**: treat response `data.token` as a secret — don't log, paste, or persist. gsk-only; not exposed in the web agent to avoid leakage via chat replays. |

### VM templates

| Subcommand | Required flags | Purpose |
|---|---|---|
| `gsk vd create_vm_template` | `--source_vm_id <id> --name <t>` | Snapshot a `ready` VM and register it as a reusable template. **Always confirm with the user before calling** — the snapshot runs 2-5 min in background. Returns `{template_id, status: "creating"}`. Poll `get_vm_template` until `status == "ready"`; `status == "failed"` surfaces the error in `error`. |
| `gsk vd list_vm_templates` | — | List all templates in the project with id, name, status, size (raw Azure SKU), vm_size (tier `lite`/`standard`/`high`), region, env_configured, ctime. |
| `gsk vd get_vm_template` | `--template_id <id>` | Full detail of a single template. |
| `gsk vd delete_vm_template` | `--template_id <id>` | Soft-delete a template. **Always confirm with the user first**. The underlying Azure snapshot is NOT deleted (resource-group cleanup only). |

## Common workflows

### Audit project health

```bash
gsk vd get_project_overview
gsk vd list_issues --status failed
gsk vd list_issues --status waiting_code_review
gsk vd list_vms
```

### Push a pending issue to an idle VM

```bash
# See what's pending
gsk vd list_issues --status pending
# See which VMs are idle (current_issue_id=null, ready_state=ready)
gsk vd list_vms
# Trigger scheduler once
gsk vd dispatch_issues
# Watch the assignment
gsk vd list_issues --status working
```

### Investigate a failing issue

```bash
gsk vd get_issue_detail --issue_id <id>       # status, work_log, test_result, pr_url
gsk vd get_pr_info --issue_id <id>            # PR state + review comments
gsk vd get_session_messages --vm_id <vm_id>   # list OpenCode sessions on that VM
gsk vd get_session_messages --vm_id <vm_id> --session_id <sid>   # full transcript
```

### Fix a VM whose preview URL / opencode session won't load

Typical symptom: the Web UI shows CORS errors hitting
`https://<domain>:8443/opencode/...`, or the VM's dev preview is
unreachable from the browser. Root cause is usually that the VM was
provisioned before the Caddy `:8443` reverse-proxy step existed, so
`/etc/caddy/conf.d/vd-preview.caddy` is missing.

```bash
# VM must be running (not suspended)
gsk vd get_vm_status --vm_id <id>
# Re-run all env setup; idempotent, ~30-60s.
gsk vd reconfigure_vm --vm_id <id>
# Retry the preview URL in the browser.
```

### Fix a VM whose GitHub token expired

```bash
gsk vd check_github_auth --repo_id <repo>            # server-side token still valid?
gsk vd refresh_vm_github_token --vm_id <vm> --repo_id <repo>   # re-inject into VM
gsk vd execute_command --vm_id <vm> --command "cd /path/to/repo && git fetch"
```

### Merge a PR from your laptop (local `gh` without pre-existing auth)

Use when your local `gh` CLI has no access to a private repo owned by
the VD GitHub App.  Mints a short-lived installation token for that
specific repo, authenticates `gh` with it, runs the merge, then the
token expires in ~1h on its own.

```bash
# Mint a token and keep only the raw string in a shell variable
TOKEN=$(gsk vd get_repo_github_token --repo_id <repo_id> | jq -r '.data.token')

# Authenticate local gh with the token (reads from stdin)
echo "$TOKEN" | gh auth login --with-token --hostname github.com

# Now normal gh commands work against this repo
gh pr merge 123 --merge --repo owner/repo

# Token expires after ~1h; re-run `gsk vd get_repo_github_token` for a fresh one.
unset TOKEN
```

**Safety**: the token is treated as a secret by the skill — don't
echo it to stdout, don't paste it into chat, don't write it to a
file on disk.  The `jq -r '.data.token'` extraction keeps it in a
shell variable only.

### Run a diagnostic command on a working VM

```bash
# VM must be ready, not suspended
gsk vd get_vm_status --vm_id <id>
gsk vd execute_command --vm_id <id> --command "git status && tmux ls" --timeout 10
```

### Save a configured VM as a template

```bash
# Always confirm with user first — takes 2-5 min in background
gsk vd create_vm_template --source_vm_id <ready-vm> --name "my-dev-env"
# Returns {template_id, status: "creating"}
# Poll:
gsk vd get_vm_template --template_id <tid>
# When status=="ready", snapshot_id is populated and it's usable in create_vm
```

## Safety rules

- **Confirm with the user before** calling `create_vm_template`, `delete_vm_template`, `delete_vm`, `vm_action --action stop`, `issue_action --action cancel/reject_merge/confirm_merge`, `update_vm_startup_script`, `create_github_issue`. These mutate state, produce user-visible side effects (PR merges, Azure resource churn, GitHub noise), or take minutes to complete.
- **Never `execute_command`** with destructive args (`rm -rf`, `git reset --hard`, `kill -9`) without an explicit ask. The VM holds user work-in-progress.
- **Before calling `refresh_vm_github_token`**, verify the VM is actually hitting 401s — do not rotate tokens pre-emptively; it invalidates any concurrent git operation on the VM.

## See also

- `../gsk-shared/SKILL.md` — auth, output conventions, global flags.
- Web UI for the same functionality: `https://<host>/virtual-developer/project/<vd_project_id>` → Agent tab.
