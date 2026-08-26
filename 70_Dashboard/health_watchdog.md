# Knowledge Base Health Watchdog Report

**Generated**: 2026-08-26 11:59:04  **Summary**: CRITICAL  (CRIT=1 WARN=0)

| Check | Status | Detail |
|---|---|---|
| git_object_store | OK | fsck connectivity clean |
| git_head_reachable | OK | HEAD history walkable (10 commits) |
| git_object_garbage | OK | no stale tmp_pack / orphan idx |
| commit_freshness | OK | last commit 0h ago |
| working_tree_backlog | OK | 15 pending change(s) |
| daily_sync | CRIT | sync started 13h ago but never completed (last done-line: 2026-07-15 00:29:50 / OK / 成功 / 2264文件) - STUCK |
| getnotes_pull | OK | last pull 13h ago, total=429 |
| pipeline | OK | last run 5.2h ago, new_papers=6 |
| config_llm_config | OK | llm_config.json valid |
| config_model_switch | OK | model_switch.json valid |
| daemons | OK | pythonw=2 node=11 preview8899=True |
| scheduled_tasks | OK | all iNEST tasks registered |
| gitee | INFO | gitee sync_time=2026-07-11T21:46:41 (script hardcodes disabled, by design) |

> Auto-generated hourly by kb_health_watchdog.ps1. CRIT items trigger auto-repair (object store -> refetch from github).
