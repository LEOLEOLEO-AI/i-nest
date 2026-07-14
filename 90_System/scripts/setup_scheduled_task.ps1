# iNEST Scheduled Task Setup — Daily Import + Gitee Sync
# Run once as Administrator to install

$action = New-ScheduledTaskAction `
    -Execute "powershell" `
    -Argument "-NoProfile -WindowStyle Hidden -File D:\Obsidian\scripts\daily_runner.ps1" `
    -WorkingDirectory "D:\Obsidian\scripts"

$trigger1 = New-ScheduledTaskTrigger -Daily -At 09:00
$trigger2 = New-ScheduledTaskTrigger -Daily -At 21:00

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -MultipleInstances IgnoreNew `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 10)

# Remove old task if exists
Unregister-ScheduledTask -TaskName "iNEST_Daily_Sync" -Confirm:$false -ErrorAction SilentlyContinue

Register-ScheduledTask `
    -TaskName "iNEST_Daily_Sync" `
    -Action $action `
    -Trigger $trigger1, $trigger2 `
    -Settings $settings `
    -Description "Daily: GetNotes import (5/20+) + Gitee auto-push for iNEST vault" `
    -User $env:USERNAME

Write-Host "Task created: iNEST_Daily_Sync (daily 09:00 + 21:00)"
Write-Host "Actions: GetNotes import -> Gitee auto-sync"