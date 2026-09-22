# Knowledge Base Health Watchdog Report

**Generated**: 2026-09-22 22:23:50  **Summary**: WARNING  (CRIT=0 WARN=3)

| Check | Status | Detail |
|---|---|---|
| git_object_store | OK | fsck connectivity clean |
| git_head_reachable | OK | HEAD history walkable (115 commits) |
| git_object_garbage | OK | no stale tmp_pack / orphan idx |
| commit_freshness | OK | last commit 17.9h ago |
| working_tree_backlog | WARN | 94 pending changes (>50, not yet committed/published) |
| github_divergence | OK | 与 github/main 同源; 本地独有 1 / 落后 0 |
| daily_sync | WARN | 同步已尝试但未完成: last start 0.000492841722222222h ago / last done 25.4h ago — 见 D:\Obsidian\scripts\sync_log.txt |
| getnotes_pull | OK | last pull 25.4h ago, total=593 |
| pipeline | OK | last run 5.4h ago, new_papers=0 (task last run 09/22/2026 16:53:33, exit=0x0) |
| config_llm_config | OK | llm_config.json valid |
| config_model_switch | OK | model_switch.json valid |
| daemons | OK | pythonw=2 node=3 preview8899=True |
| scheduled_tasks | OK | all required iNEST tasks registered / iNEST_Self_Evolve(依设计禁用: 2026-09-01 用户决定改由 WorkBuddy 自动化负责每日自进化) |
| self_evolve_outcome | WARN | 自膨胀告警: 连续 3 轮只新增不关闭 — R15: opened=1 closed=0 escalated=51 gate_new=1 open_total=80 |
| gitee | INFO | gitee sync_time=2026-07-11T21:46:41 (script hardcodes disabled, by design) |

> Auto-generated hourly by kb_health_watchdog.ps1. CRIT items trigger auto-repair (object store -> refetch from github).
