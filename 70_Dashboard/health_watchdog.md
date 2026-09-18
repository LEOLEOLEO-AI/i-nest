# Knowledge Base Health Watchdog Report

**Generated**: 2026-09-18 11:08:14  **Summary**: CRITICAL  (CRIT=1 WARN=2)

| Check | Status | Detail |
|---|---|---|
| git_object_store | OK | fsck connectivity clean |
| git_head_reachable | OK | HEAD history walkable (98 commits) |
| git_object_garbage | OK | no stale tmp_pack / orphan idx |
| commit_freshness | OK | last commit 0h ago |
| working_tree_backlog | CRIT | 6002 pending changes (>200, pipeline output likely stuck) |
| github_divergence | OK | 与 github/main 同源; 本地独有 0 / 落后 0 |
| daily_sync | WARN | 同步已尝试但未完成: last start 13.5941361205278h ago / last done 206.1h ago — 见 D:\Obsidian\scripts\sync_log.txt |
| getnotes_pull | OK | last pull 13.6h ago, total=563 |
| pipeline | OK | last run 4.4h ago, new_papers=0 (task last run 09/18/2026 06:30:01, exit=0x0) |
| config_llm_config | OK | llm_config.json valid |
| config_model_switch | OK | model_switch.json valid |
| daemons | OK | pythonw=2 node=6 preview8899=True |
| scheduled_tasks | OK | all required iNEST tasks registered / iNEST_Self_Evolve(依设计禁用: 2026-09-01 用户决定改由 WorkBuddy 自动化负责每日自进化) |
| self_evolve_outcome | WARN | 门禁有 1 项新增违规 — R7: opened=3 closed=0 escalated=55 gate_new=1 open_total=81 |
| gitee | INFO | gitee sync_time=2026-07-11T21:46:41 (script hardcodes disabled, by design) |

> Auto-generated hourly by kb_health_watchdog.ps1. CRIT items trigger auto-repair (object store -> refetch from github).
