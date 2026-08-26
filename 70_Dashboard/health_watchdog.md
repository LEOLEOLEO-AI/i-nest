# Knowledge Base Health Watchdog Report

**Generated**: 2026-08-26 12:59:03  **Summary**: OK  (CRIT=0 WARN=0)

| Check | Status | Detail |
|---|---|---|
| git_object_store | OK | fsck connectivity clean |
| git_head_reachable | OK | HEAD history walkable (11 commits) |
| git_object_garbage | OK | no stale tmp_pack / orphan idx |
| commit_freshness | OK | last commit 0.4h ago |
| working_tree_backlog | OK | 17 pending change(s) |
| daily_sync | OK | last sync start 0.4h ago, completed 0.4h ago |
| getnotes_pull | OK | last pull 0.4h ago, total=432 |
| pipeline | OK | last run 6.2h ago, new_papers=6 |
| config_llm_config | OK | llm_config.json valid |
| config_model_switch | OK | model_switch.json valid |
| daemons | OK | pythonw=2 node=10 preview8899=True |
| scheduled_tasks | OK | all iNEST tasks registered |
| gitee | INFO | gitee sync_time=2026-07-11T21:46:41 (script hardcodes disabled, by design) |

> Auto-generated hourly by kb_health_watchdog.ps1. CRIT items trigger auto-repair (object store -> refetch from github).
