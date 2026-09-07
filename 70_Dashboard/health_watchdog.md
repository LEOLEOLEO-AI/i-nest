# Knowledge Base Health Watchdog Report

**Generated**: 2026-09-08 06:46:12  **Summary**: WARNING  (CRIT=0 WARN=2)

| Check | Status | Detail |
|---|---|---|
| git_object_store | OK | fsck connectivity clean |
| git_head_reachable | OK | HEAD history walkable (85 commits) |
| git_object_garbage | OK | no stale tmp_pack / orphan idx |
| commit_freshness | WARN | no commit in 27.2h (stale > 26 h) |
| working_tree_backlog | OK | 47 pending change(s) |
| daily_sync | INFO | sync disabled (by design); last done: 2026-09-06 21:33:54 / OK / Safe sync complete: GitHub only. / last start: 2026-09-08 06:45:55 |
| getnotes_pull | WARN | last pull 33.2h ago (> 26 h) |
| pipeline | OK | last run 24.1h ago, new_papers=0 (task last run 09/08/2026 06:43:05, exit=0x800710E0 failed) |
| config_llm_config | OK | llm_config.json valid |
| config_model_switch | OK | model_switch.json valid |
| daemons | OK | pythonw=2 node=8 preview8899=True |
| scheduled_tasks | OK | all iNEST tasks registered |
| gitee | INFO | gitee sync_time=2026-07-11T21:46:41 (script hardcodes disabled, by design) |

> Auto-generated hourly by kb_health_watchdog.ps1. CRIT items trigger auto-repair (object store -> refetch from github).
