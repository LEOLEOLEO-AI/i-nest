# Gitee Daily Auto-Sync for iNEST Obsidian Vault
# Runs: git add -> commit -> pull -> push
# Repo: https://gitee.com/iBrainNest/i-nest

$vault = "D:\Obsidian\home\work\.openclaw\workspace"
$logFile = "D:\Obsidian\scripts\gitee_sync_log.txt"
$date = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Set-Location $vault

# Stage all changes
git add -A 2>&1 | Out-Null

# Check if there's anything to commit
$status = git status --porcelain
if (-not $status) {
    "$date | No changes to sync" | Out-File $logFile -Append -Encoding UTF8
    Write-Host "$date | No changes"
    exit 0
}

# Commit
git commit -m "auto-sync: $date" 2>&1 | Out-Null

# Pull first (in case of remote changes)
git pull origin main --no-rebase 2>&1 | Out-Null

# Push
$result = git push origin main 2>&1
if ($LASTEXITCODE -eq 0) {
    "$date | Push OK | $(($status -split '\n').Count) files" | Out-File $logFile -Append -Encoding UTF8
    Write-Host "$date | Synced successfully"
} else {
    "$date | Push FAILED | $result" | Out-File $logFile -Append -Encoding UTF8
    Write-Host "$date | Sync failed: $result"
}