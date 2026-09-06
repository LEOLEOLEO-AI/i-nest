# Knowledge Base Health Watchdog Report

**Generated**: 2026-09-07 02:59:04  **Summary**: OK  (CRIT=0 WARN=0)

| Check | Status | Detail |
|---|---|---|
| git_object_store | OK | fsck connectivity clean |
| git_head_reachable | OK | HEAD history walkable (84 commits) |
| git_object_garbage | OK | no stale tmp_pack / orphan idx |
| commit_freshness | OK | last commit 5.4h ago |
| working_tree_backlog | OK | 112 pending change(s) |
| daily_sync | OK | last sync completed 5.4h ago |
| getnotes_pull | OK | last pull 5.4h ago, total=495 |
| pipeline | OK | last run 3.4h ago, new_papers=2 (task last run 09/06/2026 12:28:39, exit=0xC000013A failed) |
| config_llm_config | OK | llm_config.json valid |
| config_model_switch | OK | model_switch.json valid |
| daemons | OK | pythonw=2 node=6 preview8899=True |
| scheduled_tasks | OK | all iNEST tasks registered |
| gitee | INFO | gitee sync_time=2026-07-11T21:46:41 (script hardcodes disabled, by design) |

> Auto-generated hourly by kb_health_watchdog.ps1. CRIT items trigger auto-repair (object store -> refetch from github).
