# TCC + iNEST Research Linkage — Complete Setup Guide
# Generated: 2026-07-14

## Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  10_Inbox    │────▶│  DeepSeek    │────▶│  30_TCC      │
│  (剪藏入口)   │     │  V4 Pro      │     │  40_iNEST    │
└──────────────┘     │  (Codex)     │     └──────────────┘
                     └──────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ 看板刷新  │ │ Git同步   │ │ 周度报告  │
        └──────────┘ └──────────┘ └──────────┘
```

## 1. Claudian Plugin Configuration

In Obsidian:
1. Open Settings → Community Plugins → Claudian
2. Under "Agent Configuration":
   - Agent: Codex
   - Path: C:\\Users\\LEO\\AppData\\Local\\OpenAI\\Codex\\bin\\3135b80b111fd431\\codex.exe
3. Under "Default Instructions":
   - Paste the contents of AGENTS.md
4. Hotkeys (Settings → Hotkeys):
   - "Claudian: New Chat" → Ctrl+Shift+C
   - "Claudian: Process Inbox" → Ctrl+Shift+I

## 2. One-Click Commands

Run from terminal or bind to Obsidian buttons:

```bash
# Process Inbox
python D:\Obsidian\home\work\.openclaw\workspace\90_System\scripts\quick_task.py inbox

# Full pipeline (S2 + arXiv + classify)
python D:\Obsidian\home\work\.openclaw\workspace\90_System\scripts\quick_task.py pipeline

# Git sync
python D:\Obsidian\home\work\.openclaw\workspace\90_System\scripts\quick_task.py sync

# Weekly report
python D:\Obsidian\home\work\.openclaw\workspace\90_System\scripts\quick_task.py weekly

# Health check
python D:\Obsidian\home\work\.openclaw\workspace\90_System\scripts\quick_task.py health
```

## 3. Auto-Start (Windows Task Scheduler)

```powershell
# Create scheduled task for login auto-start
$action = New-ScheduledTaskAction -Execute "D:\Obsidian\scripts\startup_linkage.bat"
$trigger = New-ScheduledTaskTrigger -AtLogon
Register-ScheduledTask -TaskName "TCC_iNEST_Linkage" -Action $action -Trigger $trigger -Description "Auto-start research linkage"
```

## 4. HTTP Preview

- Vault: http://127.0.0.1:8899
- Dashboard: http://127.0.0.1:8899/home/work/.openclaw/workspace/70_Dashboard/index.html
- Home: http://127.0.0.1:8899/home/work/.openclaw/workspace/Home.md

## 5. Quick Task List

| Task | Script | Trigger |
|------|--------|---------|
| Process Inbox | quick_task.py inbox | Manual / File watcher |
| Daily Pipeline | pipeline_v3.py | 08:00 Task Scheduler |
| Kanban Refresh | daily_kanban_update.py | 08:30 Task Scheduler |
| Git Sync | gitee_sync.py | 21:00 Task Scheduler |
| Weekly Report | progress_report.py | Sunday 03:00 |
