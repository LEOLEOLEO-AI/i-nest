# iNEST Daily Runner: GetNotes Import + Gitee Sync
# Scheduled: 09:00 and 21:00 daily

$log = "D:\Obsidian\scripts\daily_runner_log.txt"
$date = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

"$date | === Daily Runner Start ===" | Out-File $log -Append -Encoding UTF8

# Step 1: GetNotes Import
$env:PYTHONIOENCODING = 'utf-8'
$importResult = python D:\Obsidian\scripts\getnotes_importer.py 2>&1
"$date | Import: $importResult" | Out-File $log -Append -Encoding UTF8
Write-Host $importResult

# Step 2: Gitee Sync
$syncResult = & D:\Obsidian\scripts\gitee_auto_sync.ps1 2>&1
"$date | Sync: $syncResult" | Out-File $log -Append -Encoding UTF8
Write-Host $syncResult

"$date | === Daily Runner End ===" | Out-File $log -Append -Encoding UTF8