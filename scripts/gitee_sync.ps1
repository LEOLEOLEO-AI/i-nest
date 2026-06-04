# ============================================================
# Gitee 三平台同步脚本 (v2)
# 中央枢纽: https://gitee.com/iBrainNest/i-nest.git
# 平台: Obsidian | Genspark | Claw Computer
# 策略: Pull-First → 分类检测 → 分类提交 → Push
# ============================================================

param(
    [switch]$DryRun,        # 预览模式，不实际提交
    [switch]$Force,         # 跳过确认
    [switch]$StatusOnly     # 仅显示变更状态
)

$ErrorActionPreference = "Continue"

# ---- 配置 ----
$RepoPath = "D:\Obsidian\home\work\.openclaw\workspace"
$StateFile = "D:\Obsidian\scripts\gitee_sync_state.json"
$LogFile = "D:\Obsidian\scripts\gitee_sync_log.txt"
$Branch = "main"

# ---- 内容分类映射 ----
$CategoryMap = @{
    "代码"     = @("*\iNEST_4_工程开发\*", "*\TCC_4_工程开发\*", "scripts\*", "skills\*", "copilot\*")
    "论文"     = @("papers\*", "*\iNEST_2_论文撰写\*", "*\TCC_2_论文撰写\*")
    "专利"     = @("*\iNEST_3_专利撰写\*", "*\TCC_3_专利撰写\*")
    "知识库"   = @("knowledge_graph\*", "01_MOC\*", "03_Topics\*", "99_Journal\*", "inspiration_engine\*", "memory\*", "dashboard\*")
    "项目策划" = @("*\iNEST_1_项目策划\*", "*\TCC_1_项目策划\*")
    "灵感"     = @("iNEST_灵感池\*", "00_Inbox\*")
    "系统"     = @("90_System\*", ".obsidian\*", ".smart-env\*", ".tasks\*", "state\*", "skills\*")
}

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "$ts | $Level | $Message"
    Write-Host $line
    $line | Out-File $LogFile -Append -Encoding UTF8
}

function Invoke-Git {
    param([string[]]$Arguments)
    $output = & git @Arguments 2>&1
    return $output
}

function Get-SyncState {
    if (Test-Path $StateFile) {
        try { return Get-Content $StateFile -Raw | ConvertFrom-Json }
        catch { Write-Log "状态文件损坏，重建中" "WARN" }
    }
    return @{
        last_sync_time = "1970-01-01T00:00:00"
        last_sync_hash = ""
        platform = "obsidian"
        sync_count = 0
    }
}

function Save-SyncState {
    param($Hash, $Changes)
    $state = @{
        last_sync_time = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
        last_sync_hash = $Hash
        platform = "obsidian"
        sync_count = ((Get-SyncState).sync_count + 1)
        last_changes = $Changes
    }
    $state | ConvertTo-Json | Set-Content $StateFile -Encoding UTF8
}

function Get-CategoryForFile {
    param([string]$FilePath)
    $normalized = $FilePath -replace '\\', '/'
    foreach ($cat in $CategoryMap.Keys) {
        foreach ($pattern in $CategoryMap[$cat]) {
            $normPattern = $pattern -replace '\\', '/'
            if ($normalized -like $normPattern) {
                return $cat
            }
        }
    }
    return "其他"
}

# ---- 主流程 ----
Write-Log "========== 同步开始 ==========" "SYNC"

Set-Location $RepoPath

# 0. 确保在正确的分支
$currentBranch = (Invoke-Git -Arguments @("branch", "--show-current")) -join ""
if ($currentBranch -ne $Branch) {
    Write-Log "切换到 $Branch 分支" "INFO"
    Invoke-Git -Arguments @("checkout", $Branch) | Out-Null
}

# 1. Fetch 远程更新
Write-Log "Step 1/5: 获取远程更新..." "INFO"
$fetchOutput = Invoke-Git -Arguments @("fetch", "origin", $Branch)
Write-Log "远程 fetch 完成" "INFO"

# 2. 检查远程是否有新内容
$localHash = (Invoke-Git -Arguments @("rev-parse", "HEAD")) -join ""
$remoteHash = (Invoke-Git -Arguments @("rev-parse", "origin/$Branch")) -join ""
$behindCount = [int]((Invoke-Git -Arguments @("rev-list", "--count", "HEAD..origin/$Branch")) -join "")

if ($behindCount -gt 0) {
    Write-Log "Step 2/5: 发现远程 $behindCount 个新提交，拉取中..." "INFO"
    $pullResult = Invoke-Git -Arguments @("pull", "origin", $Branch, "--no-rebase")
    if ($LASTEXITCODE -ne 0) {
        Write-Log "拉取有冲突，尝试 stash → pull → pop" "WARN"
        Invoke-Git -Arguments @("stash") | Out-Null
        Invoke-Git -Arguments @("pull", "origin", $Branch, "--no-rebase") | Out-Null
        Invoke-Git -Arguments @("stash", "pop") | Out-Null
    }
    Write-Log "远程更新已合并" "OK"
} else {
    Write-Log "Step 2/5: 远程无新内容，跳过拉取" "INFO"
}

# 3. 检测本地变更
Write-Log "Step 3/5: 检测本地变更..." "INFO"
$statusOutput = Invoke-Git -Arguments @("status", "--porcelain")
$statusLines = @($statusOutput | Where-Object { $_ -and $_.Trim() -ne "" })

if ($statusLines.Count -eq 0) {
    Write-Log "没有本地变更，同步完成" "OK"
    Write-Log "========== 同步结束 (无变更) ==========" "SYNC"
    exit 0
}

# 分析变更
$added = [System.Collections.ArrayList]::new()
$modified = [System.Collections.ArrayList]::new()
$deleted = [System.Collections.ArrayList]::new()
$renamed = [System.Collections.ArrayList]::new()

foreach ($line in $statusLines) {
    $statusCode = $line.Substring(0, 2).Trim()
    $file = $line.Substring(3)
    
    if ($statusCode -match "^\?\?") {
        [void]$added.Add($file)
    } elseif ($statusCode -match "^A") {
        [void]$added.Add($file)
    } elseif ($statusCode -match "^M") {
        [void]$modified.Add($file)
    } elseif ($statusCode -match "^D") {
        [void]$deleted.Add($file)
    } elseif ($statusCode -match "^R") {
        [void]$renamed.Add($file)
    } else {
        [void]$modified.Add($file)
    }
}

# 分类统计
$categoryStats = @{}
$allChanged = @($added) + @($modified)
foreach ($f in $allChanged) {
    $cat = Get-CategoryForFile -FilePath $f
    if (-not $categoryStats[$cat]) { $categoryStats[$cat] = 0 }
    $categoryStats[$cat]++
}

# 显示变更摘要
Write-Host ""
Write-Host "========== 变更摘要 ==========" -ForegroundColor Cyan
Write-Host "  新增: $($added.Count)  修改: $($modified.Count)  删除: $($deleted.Count)" -ForegroundColor Yellow
foreach ($cat in ($categoryStats.Keys | Sort-Object)) {
    Write-Host "  [$cat] $($categoryStats[$cat]) 个文件" -ForegroundColor Green
}

if ($StatusOnly) {
    Write-Host ""
    Write-Host "详细变更列表:" -ForegroundColor Cyan
    foreach ($f in ($added | Sort-Object)) { Write-Host "  + $f" -ForegroundColor Green }
    foreach ($f in ($modified | Sort-Object)) { Write-Host "  ~ $f" -ForegroundColor Yellow }
    foreach ($f in ($deleted | Sort-Object)) { Write-Host "  - $f" -ForegroundColor Red }
    Write-Log "状态检查完成" "OK"
    exit 0
}

if ($DryRun) {
    Write-Log "预览模式，不执行实际提交" "INFO"
    Write-Log "========== 同步结束 (预览) ==========" "SYNC"
    exit 0
}

# 4. 构建提交信息
$commitParts = @()
foreach ($cat in ($categoryStats.Keys | Sort-Object)) {
    $commitParts += "[$cat]$($categoryStats[$cat])"
}
$commitMsg = "sync: $($commitParts -join ' ') - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
Write-Log "Step 4/5: 提交 ($commitMsg)" "INFO"

Invoke-Git -Arguments @("add", "-A") | Out-Null
$commitOutput = Invoke-Git -Arguments @("commit", "-m", $commitMsg)

if ($LASTEXITCODE -ne 0) {
    Write-Log "提交跳过（可能无变更）" "WARN"
}

# 5. Push
Write-Log "Step 5/5: 推送到 Gitee..." "INFO"
$pushOutput = Invoke-Git -Arguments @("push", "origin", $Branch)

if ($LASTEXITCODE -eq 0) {
    $finalHash = (Invoke-Git -Arguments @("rev-parse", "HEAD")) -join ""
    Save-SyncState -Hash $finalHash -Changes $categoryStats
    
    Write-Host ""
    Write-Host "========== 同步成功 ==========" -ForegroundColor Green
    Write-Host "  平台: Obsidian → Gitee" -ForegroundColor Green
    Write-Host "  提交: $commitMsg" -ForegroundColor Green
    Write-Host "  文件: $($allChanged.Count) 个" -ForegroundColor Green
    Write-Log "推送成功 | $($allChanged.Count) 文件 | $commitMsg" "OK"
} else {
    Write-Log "推送失败: $pushOutput" "ERROR"
    Write-Host "推送失败，可能需手动处理合并冲突" -ForegroundColor Red
}

Write-Log "========== 同步结束 ==========" "SYNC"
