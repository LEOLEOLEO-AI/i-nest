---
schema: implementation-backlog-v1
owner: codex
updated_at: 2026-09-15
---

# Research OS Implementation Backlog

## P0: Restore One Source Of Truth

- [ ] Create a single runtime config with `vault_root`, `inbox_root`, `processing_root`, `output_root`, and `local_data_roots`.
- [ ] Make every adapter emit the external tool contract package.
- [ ] Add idempotency by `source_system + source_id + content_hash`.
- [ ] Fix health-check field mismatch between `sync_state.json` and `check_sync_health.ps1`.
- [ ] Remove active references to Gitee and obsolete Agent roots from operational paths.

## P1: Turn Knowledge Into Research Work

- [ ] Generate a Research Passport from a reviewed Inbox item.
- [ ] Link hypotheses, evidence, experiments, and deliverables by stable IDs.
- [ ] Add a review queue for promotion from `00_Inbox` to canonical directories.
- [ ] Replace generic task recommendations with executable tasks containing method and acceptance.
- [ ] Add a blocked-state report for tasks without evidence or reproducible inputs.

## P2: Close The Research-to-Output Loop

- [ ] Generate experiment manifests from a passport.
- [ ] Capture code revision, configuration, seed, logs, and result paths.
- [ ] Generate paper, patent, and project-guide deliverable manifests from the same evidence ledger.
- [ ] Add a weekly cross-domain review for TCC/iNEST bridge hypotheses.

## First Demonstrator

Use one bounded task rather than migrating the whole vault:

`TCC-I-20260915-001`

Question: whether a reconfigurable topology changes the measured behavior of
an event-driven network under fixed workload and fixed compute resources.

Required first artifacts:

- question card
- evidence ledger
- experiment card
- reproducible run manifest
- one figure
- one decision note

All quantitative results remain `[待测]` until the run is executed and logged.
