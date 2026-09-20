# Knowledge Base Health Watchdog Report

**Generated**: 2026-09-20 07:59:08  **Summary**: OK  (CRIT=0 WARN=0)

| Check | Status | Detail |
|---|---|---|
| git_object_store | OK | fsck connectivity clean |
| git_head_reachable | OK | HEAD history walkable (110 commits) |
| git_object_garbage | OK | no stale tmp_pack / orphan idx |
| commit_freshness | OK | last commit 3.5h ago |
| working_tree_backlog | OK | 37 pending change(s) |
| github_divergence | OK | 与 github/main 同源; 本地独有 1 / 落后 0 |
| daily_sync | OK | last sync completed 21.1h ago |
| getnotes_pull | OK | last pull 21.2h ago, total=572 |
| pipeline | OK | last run 1.2h ago, new_papers=0 (task last run 09/20/2026 06:30:01, exit=0x0) |
| config_llm_config | OK | llm_config.json valid |
| config_model_switch | OK | model_switch.json valid |
| daemons | OK | pythonw=2 node=3 preview8899=True |
| scheduled_tasks | OK | all required iNEST tasks registered / iNEST_Self_Evolve(依设计禁用: 2026-09-01 用户决定改由 WorkBuddy 自动化负责每日自进化) |
| self_evolve_outcome | OK | 3.5h 前运行 — R12: opened=3 closed=1 escalated=48 gate_new=0 open_total=77 |
| gitee | INFO | gitee sync_time=2026-07-11T21:46:41 (script hardcodes disabled, by design) |

> Auto-generated hourly by kb_health_watchdog.ps1. CRIT items trigger auto-repair (object store -> refetch from github).
