# Knowledge Base Health Watchdog Report

**Generated**: 2026-09-17 07:24:05  **Summary**: WARNING  (CRIT=0 WARN=1)

| Check | Status | Detail |
|---|---|---|
| git_object_store | OK | fsck connectivity clean |
| git_head_reachable | OK | HEAD history walkable (89 commits) |
| git_object_garbage | OK | no stale tmp_pack / orphan idx |
| commit_freshness | WARN | no commit in 47.1h (stale > 26 h) |
| working_tree_backlog | OK | 178 pending change(s) |
| daily_sync | INFO | sync disabled (by design); last done: 2026-09-09 21:00:38 / OK / Safe sync complete: GitHub only. / last start: 2026-09-16 21:00:01 |
| getnotes_pull | OK | last pull 10.4h ago, total=555 |
| pipeline | OK | last run 15.1h ago, new_papers=8 (task last run 09/17/2026 06:41:25, exit=0x41301 failed) |
| config_llm_config | OK | llm_config.json valid |
| config_model_switch | OK | model_switch.json valid |
| daemons | OK | pythonw=2 node=2 preview8899=True |
| scheduled_tasks | OK | all iNEST tasks registered |
| gitee | INFO | gitee sync_time=2026-07-11T21:46:41 (script hardcodes disabled, by design) |

> Auto-generated hourly by kb_health_watchdog.ps1. CRIT items trigger auto-repair (object store -> refetch from github).
