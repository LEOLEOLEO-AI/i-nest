# Knowledge Base Health Watchdog Report

**Generated**: 2026-09-26 11:59:11  **Summary**: WARNING  (CRIT=0 WARN=3)

| Check | Status | Detail |
|---|---|---|
| git_object_store | OK | fsck connectivity clean |
| git_head_reachable | OK | HEAD history walkable (121 commits) |
| git_object_garbage | OK | no stale tmp_pack / orphan idx |
| commit_freshness | OK | last commit 13.3h ago |
| working_tree_backlog | WARN | 125 pending changes (>50, not yet committed/published) |
| github_divergence | OK | 与 github/main 同源; 本地独有 0 / 落后 0 |
| daily_sync | OK | last sync completed 13.3h ago |
| getnotes_pull | OK | last pull 13.3h ago, total=619 |
| pipeline | OK | last run 1.2h ago, new_papers=0 (task last run 09/26/2026 10:30:56, exit=0x0) |
| config_llm_config | OK | llm_config.json valid |
| config_model_switch | OK | model_switch.json valid |
| daemons | OK | pythonw=2 node=2 preview8899=True |
| scheduled_tasks | WARN | missing/unexpectedly disabled: TCC_iNEST_Linkage(Disabled) |
| self_evolve_outcome | WARN | 自膨胀告警: 连续 6 轮只新增不关闭 — R18: opened=2 closed=0 escalated=56 gate_new=1 open_total=84 |
| gitee | INFO | gitee sync_time=2026-07-11T21:46:41 (script hardcodes disabled, by design) |

> Auto-generated hourly by kb_health_watchdog.ps1. CRIT items trigger auto-repair (object store -> refetch from github).
