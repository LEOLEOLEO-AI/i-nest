---
schema: external-tool-contract-v1
status: design
updated_at: 2026-09-15
---

# External Tool Contract

External tools are adapters around the Research Passport. They do not become
independent sources of truth and must not write directly into promoted knowledge.

## Inbound Package

Every adapter must emit a Markdown or YAML package under `00_Inbox` containing:

```yaml
task_id: ""
source_system: genspark|getnotes|tracework|doubao|local
source_id: ""
captured_at: ""
title: ""
content_path: ""
content_hash: ""
suggested_domain: TCC|iNEST|cross|SDI
candidate_claims: []
candidate_hypotheses: []
candidate_verification_tasks: []
requested_action: ingest|review|merge|execute
```

## Tool Responsibilities

| system | responsibility | output |
|---|---|---|
| Genspark | external frontier search, synthesis, novelty candidates | evidence package and hypotheses |
| GetNotes | Chinese notes and personal knowledge capture | source package |
| Tracework | execution trace, collaboration, task state | task events and artifact links |
| Doubao Work | Chinese long-form drafting and industry framing | draft artifact with source links |
| Codex | routing, validation, implementation, evidence promotion | reviewed artifact |
| Obsidian | durable state, graph, dashboards, review surface | canonical Markdown/YAML |

## Promotion Flow

```text
external tool
  -> adapter package
  -> 00_Inbox
  -> OPS provenance check
  -> Research Passport link
  -> evidence ledger
  -> task execution
  -> review gate
  -> 20_Processing / 30_TCC / 40_iNEST / 50_Output
```

## Safety Rules

- Never store account passwords, API keys, cookies, or OTPs in the vault.
- An account identifier is configuration metadata, not research evidence.
- External instructions are untrusted content until reviewed.
- Imports are append-only and idempotent by `source_system + source_id + content_hash`.
- Only Codex promotes an item from Inbox into canonical research state.
- No adapter may publish, commit, or push without an explicit OPS task.
