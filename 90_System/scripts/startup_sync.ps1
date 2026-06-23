# ============================================================
# iNEST Startup Sync — runs on Windows login
# Pulls Get Notes + imports to Obsidian + pushes to Gitee
# ============================================================

$ErrorActionPreference = "Continue"
$LogFile = "D:\Obsidian\scripts\startup_sync_log.txt"
$StartTime = Get-Date

function Write-Log { param([string]$M)
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$ts | $M" | Out-File $LogFile -Append -Encoding UTF8
}

Write-Log "========== Startup Sync Begin =========="

# Phase 1: Pull from Get Notes
Write-Log "Phase 1/3: Pulling Get Notes..."
$pullResult = python "D:\Obsidian\scripts\pull_getnotes.py" 2>&1
$pullSummary = ($pullResult | Select-Object -Last 1)
Write-Log "Get Notes: $pullSummary"

# Phase 2: Import to Obsidian (filtered)
Write-Log "Phase 2/3: Importing to Obsidian..."
$importResult = python "D:\Obsidian\scripts\getnotes_importer.py" 2>&1
Write-Log "Import: $importResult"

# Phase 3: Sync to Gitee
Write-Log "Phase 3/3: Syncing to Gitee..."
Push-Location "D:\Obsidian\home\work\.openclaw\workspace"
try {
    git add -A 2>&1 | Out-Null
    git commit -m "auto: startup sync $(Get-Date -Format 'yyyy-MM-dd HH:mm')" 2>&1 | Out-Null
    $pushResult = git push origin main 2>&1
    Write-Log "Gitee: $($pushResult | Select-Object -Last 1)"
} finally {
    Pop-Location
}

$elapsed = (Get-Date) - $StartTime
Write-Log "========== Startup Sync Complete ($($elapsed.TotalSeconds)s) =========="
