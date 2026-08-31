# Knowledge Base Health Watchdog Report

**Generated**: 2026-09-01 03:59:06  **Summary**: WARNING  (CRIT=0 WARN=1)

| Check | Status | Detail |
|---|---|---|
| git_object_store | OK | fsck connectivity clean |
| git_head_reachable | OK | HEAD history walkable (49 commits) |
| git_object_garbage | OK | no stale tmp_pack / orphan idx |
| commit_freshness | OK | last commit 12.1h ago |
| working_tree_backlog | WARN | 497 pending changes (>200, possible stuck pipeline output) |
| daily_sync | OK | last sync completed 20.4h ago |
| getnotes_pull | OK | last pull 7h ago, total=456 |
| pipeline | OK | last run 21.1h ago, new_papers=0 |
| config_llm_config | OK | llm_config.json valid |
| config_model_switch | OK | model_switch.json valid |
| daemons | OK | pythonw=2 node=5 preview8899=True |
| scheduled_tasks | OK | all iNEST tasks registered |
| gitee | INFO | gitee sync_time=2026-07-11T21:46:41 (script hardcodes disabled, by design) |

> Auto-generated hourly by kb_health_watchdog.ps1. CRIT items trigger auto-repair (object store -> refetch from github).
