# Setup Windows Task Scheduler for daily pipeline
# Run: powershell -ExecutionPolicy Bypass -File setup_scheduler.ps1

$python = "D:\Obsidian\home\work\.openclaw\workspace\.venv\Scripts\python.exe"
$pipeline = "D:\Obsidian\home\work\.openclaw\workspace\90_System\scripts\pipeline.py"
$workdir = "D:\Obsidian\home\work\.openclaw\workspace"

# Daily crawl + process at 8:00 AM
$action1 = New-ScheduledTaskAction -Execute $python -Argument "`"$pipeline`" daily" -WorkingDirectory $workdir
$trigger1 = New-ScheduledTaskTrigger -Daily -At 8:00AM
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName "iNEST_Daily_Crawl" -Action $action1 -Trigger $trigger1 -Settings $settings -Description "Daily 8AM literature crawl + inbox processing" -Force

# Bi-hourly inbox check (9AM-11PM)
$action2 = New-ScheduledTaskAction -Execute $python -Argument "`"$pipeline`" process" -WorkingDirectory $workdir
$trigger2 = New-ScheduledTaskTrigger -Daily -At 9:00AM -RepetitionInterval (New-TimeSpan -Hours 2) -RepetitionDuration (New-TimeSpan -Hours 14)
Register-ScheduledTask -TaskName "iNEST_Inbox_Check" -Action $action2 -Trigger $trigger2 -Settings $settings -Description "Bi-hourly inbox processing" -Force

# Weekly full rebuild (Sunday 3AM)
$action3 = New-ScheduledTaskAction -Execute $python -Argument "`"$pipeline`" full" -WorkingDirectory $workdir
$trigger3 = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 3:00AM
Register-ScheduledTask -TaskName "iNEST_Weekly_Full" -Action $action3 -Trigger $trigger3 -Settings $settings -Description "Weekly full pipeline rebuild" -Force

Write-Host "Scheduled tasks created:"
Write-Host "  iNEST_Daily_Crawl   - Daily 8:00 AM"
Write-Host "  iNEST_Inbox_Check   - Every 2 hours (9AM-11PM)"
Write-Host "  iNEST_Weekly_Full   - Sunday 3:00 AM"
Write-Host ""
Write-Host "Manage tasks: taskschd.msc"
