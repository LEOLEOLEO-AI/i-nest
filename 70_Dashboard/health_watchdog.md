# Knowledge Base Health Watchdog Report

**Generated**: 2026-09-15 08:12:39  **Summary**: WARNING  (CRIT=0 WARN=3)

| Check | Status | Detail |
|---|---|---|
| git_object_store | OK | fsck connectivity clean |
| git_head_reachable | OK | HEAD history walkable (88 commits) |
| git_object_garbage | OK | no stale tmp_pack / orphan idx |
| commit_freshness | WARN | no commit in 131.2h (stale > 26 h) |
| working_tree_backlog | WARN | 305 pending changes (>200, possible stuck pipeline output) |
| daily_sync | INFO | sync disabled (by design); last done: 2026-09-09 21:00:38 / OK / Safe sync complete: GitHub only. / last start: 2026-09-15 08:12:15 |
| getnotes_pull | WARN | last pull 48.9h ago (> 26 h) |
| pipeline | OK | last run 23.7h ago, new_papers=0 (task last run 09/15/2026 08:08:20, exit=0x41301 failed) |
| config_llm_config | OK | llm_config.json valid |
| config_model_switch | OK | model_switch.json valid |
| daemons | OK | pythonw=2 node=4 preview8899=True |
| scheduled_tasks | OK | all iNEST tasks registered |
| gitee | INFO | gitee sync_time=2026-07-11T21:46:41 (script hardcodes disabled, by design) |

> Auto-generated hourly by kb_health_watchdog.ps1. CRIT items trigger auto-repair (object store -> refetch from github).
