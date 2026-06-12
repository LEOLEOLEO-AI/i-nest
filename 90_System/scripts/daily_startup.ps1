# ============================================================
# iNEST Daily Startup Orchestrator v1.0
# Triggered on: System startup / user login / scheduled task
# ============================================================
param(
    [switch]$SkipCrawl,
    [switch]$SkipSync,
    [switch]$NoDashboard
)

$ErrorActionPreference = "Continue"
$StartTime = Get-Date
$LogFile = "D:\Obsidian\scripts\daily_startup_log.txt"
$Today = Get-Date -Format "yyyy-MM-dd"

function Write-Log { param([string]$M, [string]$L="INFO")
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $l = "$ts | $L | $M"
    Write-Host $l
    $l | Out-File $LogFile -Append -Encoding UTF8
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  iNEST Daily Startup — $Today" -ForegroundColor Cyan
Write-Host "  TCC x iNEST Research Automation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Log "========== Daily Startup Begin ==========" "START"

# ---- Phase 1: Research Crawl + Atomize ----
if (-not $SkipCrawl) {
    Write-Host "Phase 1/4: Research Crawl" -ForegroundColor Yellow
    Write-Log "Phase 1/4: Running iNEST crawler" "INFO"
    
    $crawlResult = python "D:\Obsidian\scripts\iNEST_crawler.py" 2>&1
    $exitCode = $LASTEXITCODE
    
    # Atomize: convert crawl output to atomic Obsidian notes with wiki links
    Write-Host "  Atomizing papers..." -ForegroundColor Gray
    $atomizeResult = python "D:\Obsidian\scripts\paper_atomizer.py" 2>&1
    Write-Host $atomizeResult
    
    Write-Host $crawlResult
    if ($exitCode -eq 0) {
        Write-Log "Crawl completed successfully" "OK"
    } else {
        Write-Log "Crawl completed with exit code $exitCode" "WARN"
    }
} else {
    Write-Log "Phase 1/4: Crawl SKIPPED" "SKIP"
}

# ---- Phase 2: Dashboard Update ----
Write-Host ""
Write-Host "Phase 2/4: Update Dashboard" -ForegroundColor Yellow
Write-Log "Phase 2/4: Updating dashboard" "INFO"

$dashResult = python "D:\Obsidian\scripts\update_dashboard.py" 2>&1
Write-Host $dashResult
Write-Log "Dashboard updated" "OK"

# ---- Phase 3: Knowledge Sync ----
if (-not $SkipSync) {
    Write-Host ""
    Write-Host "Phase 3/4: Knowledge Sync to Gitee" -ForegroundColor Yellow
    Write-Log "Phase 3/4: Running gitee sync" "INFO"
    
    $syncResult = powershell -ExecutionPolicy Bypass -File "D:\Obsidian\scripts\gitee_sync.ps1" 2>&1
    Write-Host $syncResult
    Write-Log "Gitee sync completed" "OK"
} else {
    Write-Log "Phase 3/4: Sync SKIPPED" "SKIP"
}

# ---- Phase 4: Open Dashboard ----
if (-not $NoDashboard) {
    Write-Host ""
    Write-Host "Phase 4/4: Opening Dashboard" -ForegroundColor Yellow
    Write-Log "Phase 4/4: Opening dashboard" "INFO"
    
    $dashboardPath = "D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html"
    if (Test-Path $dashboardPath) {
        Start-Process $dashboardPath
        Write-Log "Dashboard opened in browser" "OK"
    } else {
        Write-Log "Dashboard file not found: $dashboardPath" "ERROR"
    }
} else {
    Write-Log "Phase 4/4: Dashboard SKIPPED" "SKIP"
}

# ---- Summary ----
$Elapsed = (Get-Date) - $StartTime
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Daily Startup Complete!" -ForegroundColor Green
Write-Host "  Duration: $($Elapsed.TotalSeconds.ToString('0.0'))s" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Log "========== Daily Startup End ($($Elapsed.TotalSeconds)s) ==========" "COMPLETE"

