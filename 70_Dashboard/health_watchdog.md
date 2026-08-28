# Knowledge Base Health Watchdog Report

**Generated**: 2026-08-27 23:43:26  **Summary**: OK  (CRIT=0 WARN=0)

| Check | Status | Detail |
|---|---|---|
| git_object_store | OK | fsck connectivity clean |
| git_head_reachable | OK | HEAD history walkable (29 commits) |
| git_object_garbage | OK | no stale tmp_pack / orphan idx |
| commit_freshness | OK | last commit 10.5h ago |
| working_tree_backlog | OK | 59 pending change(s) |
| daily_sync | OK | last sync start 24.7h ago, completed 24.6h ago |
| getnotes_pull | OK | last pull 24.7h ago, total=434 |
| pipeline | OK | last run 17h ago, new_papers=7 |
| config_llm_config | OK | llm_config.json valid |
| config_model_switch | OK | model_switch.json valid |
| daemons | OK | pythonw=2 node=1 preview8899=True |
| scheduled_tasks | OK | all iNEST tasks registered |
| gitee | INFO | gitee sync_time=2026-07-11T21:46:41 (script hardcodes disabled, by design) |

> Auto-generated hourly by kb_health_watchdog.ps1. CRIT items trigger auto-repair (object store -> refetch from github).
