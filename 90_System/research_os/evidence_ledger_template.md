---
schema: evidence-ledger-v1
task_id: ""
status: draft
updated_at: ""
---

# Evidence Ledger

This ledger is the evidence boundary for one Research Passport.
Claims without a row here must not be promoted to established results.

| claim_id | claim | evidence_label | source_or_method | verification_task_id | acceptance_criterion | status | limitations |
|---|---|---|---|---|---|---|---|
| C-001 |  | [待测] |  | V-XX01 |  | planned |  |

## Source Records

| source_id | source_system | source_locator | captured_at | integrity | notes |
|---|---|---|---|---|---|
| S-001 |  |  |  | unchecked |  |

## Promotion Rules

- `[引用]` requires a DOI, arXiv identifier, publisher record, or stable URL.
- `[仿真]` requires code version, configuration, input data, random seed, and raw log.
- `[实测]` requires instrument or hardware context and measurement procedure.
- `[推导]` requires definitions, assumptions, boundary conditions, and derivation steps.
- `[待测]` is allowed for a defined metric, but cannot be presented as a result.
