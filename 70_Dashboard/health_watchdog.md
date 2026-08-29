# Knowledge Base Health Watchdog Report

**Generated**: 2026-08-29 10:59:10  **Summary**: OK  (CRIT=0 WARN=0)

| Check | Status | Detail |
|---|---|---|
| git_object_store | OK | fsck connectivity clean |
| git_head_reachable | OK | HEAD history walkable (33 commits) |
| git_object_garbage | OK | no stale tmp_pack / orphan idx |
| commit_freshness | OK | last commit 7.4h ago |
| working_tree_backlog | OK | 32 pending change(s) |
| daily_sync | OK | last sync start 14h ago, completed 14h ago |
| getnotes_pull | OK | last pull 14h ago, total=440 |
| pipeline | OK | last run 4.3h ago, new_papers=7 |
| config_llm_config | OK | llm_config.json valid |
| config_model_switch | OK | model_switch.json valid |
| daemons | OK | pythonw=2 node=2 preview8899=True |
| scheduled_tasks | OK | all iNEST tasks registered |
| gitee | INFO | gitee sync_time=2026-07-11T21:46:41 (script hardcodes disabled, by design) |

> Auto-generated hourly by kb_health_watchdog.ps1. CRIT items trigger auto-repair (object store -> refetch from github).
