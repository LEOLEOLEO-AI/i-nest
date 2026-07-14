---
name: agentbase
version: 1.0.0
description: >-
  AgentBase (AgentDB) workspace operations from inside a CustomWorkflowAgentV2
  / OpenCode sandbox. Wraps the backend ``sandbox-mcp`` HTTP endpoint so the
  workflow agent can refresh external-data views, write workspace tables,
  and update workspace notes — exactly the operations the AgentDB chat
  sandbox exposes via its MCP server, but reachable via plain ``curl``
  because the workflow sandbox doesn't mount MCP servers.
metadata:
  category: agentdb
  requires:
    bins:
      - curl
      - jq
---

# agentbase

**PREREQUISITE:** Read `../gsk-shared/SKILL.md` for global flags. This
skill does NOT use the `gsk` CLI — there is no `gsk agentbase`
subcommand yet. Use the `curl` invocations below instead. They hit the
same backend the AgentDB chat sandbox uses, so behavior matches
``agentdb_import_external_data`` / ``agentdb_update_notes`` from that
surface 1:1.

## Why curl (and not a gsk subcommand)

The workflow sandbox (`CustomWorkflowAgentV2` → Novita) starts an
OpenCode runtime whose `opencode.json` does NOT register any MCP
servers (see `backend/openclaw/route.py::_build_opencode_config`).
That means AgentDB MCP tools — `import_external_data`, `create_view`,
`update_notes`, etc. — are NOT auto-available the way they are in the
AgentDB chat sandbox. We reach the same backend via its HTTP shim
instead: every MCP tool name maps 1:1 to a path under
`POST /api/agentdb/sandbox-mcp/<tool_name>`, authenticated with the
same `GSK_API_KEY` already in your environment.

## Auth + endpoint shape

Every call:

```
POST  ${GSK_BASE_URL}/api/agentdb/sandbox-mcp/<tool_name>
Authorization: Bearer ${GSK_API_KEY}
Content-Type: application/json

{
  "workspace_id": "<workspace_uuid from the prompt>",
  "project_id":   "",                  // ok to leave empty for headless workflows
  "arguments":    { ...per-tool args... }
}
```

Response (success):

```json
{
  "content": "<human-readable result string OR JSON-encoded payload>"
}
```

**Failure shapes are NOT uniform — DO NOT rely on a single
`^Error:` prefix check.** The backend emits at least four distinct
failure shapes (see `backend/agentdb/sandbox_api.py` and
`backend/agentdb/sandbox_mcp/agentdb_mcp.py::_call_backend`):

| Shape | Source | Example |
|---|---|---|
| `{"content": "Error: ..."}` | Most adaptor exceptions, missing-arg validations | `"Error: 'connection_id', 'query', and 'view_name' are required for create_view."` |
| `{"content": "Only workspace owners can perform this action."}` | Role gate at `sandbox_api.py:2241` — **no `Error:` prefix** | viewer/editor hitting a write action |
| `{"content": "Unknown tool: ..."}` | Dispatch miss at `sandbox_api.py:535` | typo'd tool_name |
| `{"error": "Backend returned HTTP <code>: ..."}` | Transport / 4xx / 5xx — different key | 401 from bad token, 503 from outage |
| Empty `content` | Adaptor returned `Message(content="")` — rare but possible | malformed handler return |

`jq -r .content` alone misses three of these. Use the
``_sbmcp_ok`` helper below — it checks all five at once.

Also: HTTP status is **usually 200** even on domain errors because
the backend returns failure as a normal `{"content": ...}` JSON body
(mirrors the chat-side adaptor). The `{"error": "..."}` shape with a
non-200 status only comes from transport-level failures.

`GSK_API_KEY` and `GSK_BASE_URL` are already set in the sandbox shell
(see `backend/opencode_workflows/opencode_execution_mixin.py:1821-1825`)
— don't try to refresh / rotate them.

## Get the workspace's external data connections (read-only)

Before refreshing views you usually want the connection IDs once. The
prompt may already include them, but if not:

```bash
curl -sS -X POST "${GSK_BASE_URL}/api/agentdb/sandbox-mcp/import_external_data" \
  -H "Authorization: Bearer ${GSK_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "workspace_id": "WORKSPACE_ID_HERE",
    "project_id": "",
    "arguments": { "action": "list_connections" }
  }' | jq -r .content
```

## Refresh / materialize an external-source view → workspace table

This is the **primary** operation for "scheduled dashboard refresh"
workflows. It runs a read-only SQL query against the **external**
connection (ClickHouse, Postgres, Snowflake, etc.) and writes the
result rows into a workspace table named `view_name`. Result is capped
at 50,000 rows; queries must be `SELECT` or `WITH … SELECT` only.

```bash
curl -sS -X POST "${GSK_BASE_URL}/api/agentdb/sandbox-mcp/import_external_data" \
  -H "Authorization: Bearer ${GSK_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "$(jq -nc \
        --arg ws "WORKSPACE_ID_HERE" \
        --arg conn "CONNECTION_ID_HERE" \
        --arg view "destination_table_name" \
        --arg query "SELECT count() AS total_events FROM analytics.product_events WHERE product='agentbase'" \
        '{
          workspace_id: $ws,
          project_id: "",
          arguments: {
            action: "create_view",
            connection_id: $conn,
            view_name: $view,
            query: $query
          }
        }')" | jq -r .content
```

Use `jq -nc` to build the body so embedded quotes, newlines and
ClickHouse functions (e.g. `toString(min(event_time))`) survive
without shell-escape gymnastics. The `query` field is sent verbatim to
the external DB — use that DB's SQL dialect (ClickHouse functions for
a ClickHouse connection, etc.).

**Bulk refresh pattern** (this is what the `[AgentDB] Hourly Refresh`
workflows do): wrap the call in a bash loop, capture pass/fail per
item, print a summary at the end. Do NOT abort the whole run on one
failure — record it and continue.

Define a single helper `_sbmcp_call` that handles all five failure
shapes (top-level `error`, HTTP non-2xx, empty `content`,
`Error: ...` prefix, and the `Only workspace owners ...` /
`Unknown tool: ...` / `not authorized` / `Not authorized` strings
that don't carry an `Error:` prefix). It echoes the raw response
body on stdout and exits non-zero on any failure:

```bash
# Returns 0 on success, non-zero on any failure shape.
# Echoes the response body to stdout either way (the caller can
# inspect it to attribute the failure).
_sbmcp_call() {
  local tool_name="$1"
  local body="$2"
  local http_code resp
  resp=$(curl -sS -w '\n%{http_code}' -X POST \
    "${GSK_BASE_URL}/api/agentdb/sandbox-mcp/${tool_name}" \
    -H "Authorization: Bearer ${GSK_API_KEY}" \
    -H "Content-Type: application/json" \
    -d "$body")
  http_code=$(printf '%s' "$resp" | tail -n1)
  resp=$(printf '%s' "$resp" | sed '$d')
  printf '%s\n' "$resp"
  # Transport-level failure (HTTP non-2xx).
  if [ "$http_code" -lt 200 ] || [ "$http_code" -ge 300 ]; then
    return 1
  fi
  # Top-level "error" key (e.g. {"error": "Backend returned HTTP ..."}).
  if printf '%s' "$resp" | jq -e 'has("error")' >/dev/null 2>&1; then
    return 2
  fi
  # Pull .content as a string; treat missing/empty/null as failure.
  local content
  content=$(printf '%s' "$resp" | jq -r '.content // ""')
  if [ -z "$content" ]; then
    return 3
  fi
  # Known failure-string patterns that don't use an "Error:" prefix.
  # Case-insensitive match — backend adaptors are inconsistent.
  if printf '%s' "$content" | grep -qiE '^(Error:|Unknown tool:|Only workspace owners|Not authorized|not login|permission denied)'; then
    return 4
  fi
  return 0
}

set +e
pass=0; fail=0
errors=""
for spec in \
  "pe_agentbase_kpis|SELECT count() AS total_events, ..." \
  "pe_payment_kpis|SELECT count() AS total_events, ..." \
  ; do
  view="${spec%%|*}"
  query="${spec#*|}"
  body=$(jq -nc \
    --arg ws "WORKSPACE_ID_HERE" \
    --arg conn "CONNECTION_ID_HERE" \
    --arg view "$view" \
    --arg query "$query" \
    '{workspace_id:$ws, project_id:"", arguments:{action:"create_view", connection_id:$conn, view_name:$view, query:$query}}')
  out=$(_sbmcp_call "import_external_data" "$body")
  rc=$?
  if [ "$rc" -eq 0 ]; then
    pass=$((pass+1))
  else
    fail=$((fail+1))
    # Compress the failure body to a single line for the summary.
    snippet=$(printf '%s' "$out" | tr '\n' ' ' | cut -c1-200)
    errors="${errors}
  - ${view} (rc=${rc}): ${snippet}"
  fi
done
echo "refreshed: ${pass} pass, ${fail} fail"
[ "$fail" -gt 0 ] && printf 'failures:%s\n' "$errors"
```

`rc` values from `_sbmcp_call` map 1:1 to the five failure shapes in
the table above:
`1` = HTTP non-2xx (transport),
`2` = top-level `error` key,
`3` = empty / missing `.content`,
`4` = recognised failure-string in `.content` (Error:/Unknown tool/
Only workspace owners/Not authorized/permission denied),
`0` = success.

When you need to differentiate failure causes (e.g. log auth vs
schema errors separately), branch on `rc`.

## Update workspace notes (record run metadata)

Use to record `last_refresh` timestamps, run-summary blurbs, anything
the user wants surfaced on the workspace UI's Notes panel. The
backend MERGES the JSON you send into the existing notes blob (so
sending one key only updates that key — other keys persist).

```bash
NOTES_PATCH=$(jq -nc \
  --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --arg summary "Refreshed 27 dashboards (26 pass, 1 fail)." \
  '{ product_dashboards: { last_refresh: $ts, last_summary: $summary } }')

curl -sS -X POST "${GSK_BASE_URL}/api/agentdb/sandbox-mcp/update_notes" \
  -H "Authorization: Bearer ${GSK_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "$(jq -nc --arg ws "WORKSPACE_ID_HERE" --argjson notes "$NOTES_PATCH" \
        '{workspace_id:$ws, project_id:"", arguments:{notes:$notes}}')" \
  | jq -r .content
```

If you accidentally pass `notes` as a JSON-stringified blob instead of
an object, the backend tolerates it (see
`sandbox_api._coerce_object_arg` in tests/test_agentdb_sandbox_mcp_handler_hardening.py)
— but the canonical form is a JSON object as shown.

## Other tool_names you can reach the same way

Same `/api/agentdb/sandbox-mcp/<tool_name>` shape, different
`arguments`. The full list comes from the
``TOOLS`` definition in `backend/agentdb/sandbox_mcp/agentdb_mcp.py`.
The most useful for workflows:

| `tool_name` | What it does | Typical args |
|---|---|---|
| `import_external_data` | Multiplexer for the 10 external-data actions (list_connections / inspect / preview / import / sync / sync_status / create_connection / attach_personal_source / create_view) | `{ "action": "...", ...action-specific }` |
| `create_view` | Top-level alias for the action above. Available after PR #37264 lands in your environment. | `{ "connection_id", "view_name", "query" }` |
| `get_schema` | Inspect workspace DB schema (tables, columns, row counts) | `{ "table_name": "..." }` (optional — omit for all tables) |
| `execute_sql` | Run DDL/DML against the **workspace** DB (not the external source). Use this for one-off cleanup, not bulk dashboard refresh. | `{ "sql": "..." }` |
| `preview_data` | Sample N rows from a workspace table | `{ "table_name": "...", "limit": 10 }` |
| `update_notes` | Merge a JSON patch into the workspace notes blob | `{ "notes": { ... } }` |

`create_view` as a top-level tool name is the more discoverable form;
if your backend doesn't have it yet (PR #37264 not deployed),
fall through to `import_external_data` with `action=create_view` —
they hit the same handler.

## Error patterns you will see

| Error string | What it means | What to do |
|---|---|---|
| `Error: 'connection_id', 'query', and 'view_name' are required for create_view.` | Missing one of the three required fields | Re-send with all three populated |
| `Error: connection not found: <id>` | The connection_id no longer exists in the workspace (was deleted / never matched the owner) | Call `list_connections` to find the current ID; do NOT hard-code old IDs |
| `Error: Only workspace owners can perform this action.` | You're acting as a viewer/editor, not owner. Most write actions (`create_view`, `import`, `sync`, `execute_sql` DDL, `update_notes`) require owner. | Surface the error to the user — there's no API-side workaround. |
| `Error: only SELECT queries are allowed` | The `query` contains DDL/DML (INSERT/UPDATE/DELETE/DROP). `create_view` only accepts read-only SQL. | Rewrite as `SELECT` — if you need to MODIFY the source DB, you want `execute_write` or a different connector, NOT `create_view`. |
| `Error: <connector> does not support execute_query` | Connector is mirror-only (e.g. HubSpot personal-source MCPs) — no ad-hoc SQL surface | Use `action=import` instead (full mirror) or pick a different connector |
| HTTP 401 / `Authorization` errors | `GSK_API_KEY` not exported into the subprocess that's running curl | Echo `printenv GSK_API_KEY \| head -c 8` (truncated for safety) to confirm the env var made it into your shell — should print `gsk-...` |

## See also

- `../gsk-shared/SKILL.md` — global flags + auth (note: this skill
  doesn't use the gsk CLI, but the auth model is the same).
- `backend/agentdb/sandbox_mcp/agentdb_mcp.py` — canonical list of
  every `tool_name` reachable via this endpoint shape, with input
  schemas.
- `backend/agentdb/sandbox_api.py` — the FastAPI router that backs
  `POST /api/agentdb/sandbox-mcp/<tool_name>`.

