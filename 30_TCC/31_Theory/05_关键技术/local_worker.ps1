param(
  [Parameter(Mandatory = $true)][string]$JobFile
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $JobFile)) {
  Write-Host "ERROR: Job file not found: $JobFile" -ForegroundColor Red
  exit 2
}

$job = Get-Content -Raw -Encoding UTF8 $JobFile | ConvertFrom-Json
$task = $job.task
$args = $job.args

$vaultRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

function Invoke-Exe([string]$file, [object[]]$argList, [string]$cwd) {
  Push-Location $cwd
  try {
    $script:lastOutput = @(& $file @argList 2>&1)
    return $LASTEXITCODE
  }
  finally {
    Pop-Location
  }
}

function Find-File([string]$root, [string]$name, [string]$mustContain) {
  $m = Get-ChildItem -Path $root -Recurse -File -Filter $name -ErrorAction SilentlyContinue | Where-Object { $_.FullName -like "*$mustContain*" } | Select-Object -First 1
  if ($m) { return $m.FullName }
  $m2 = Get-ChildItem -Path $root -Recurse -File -Filter $name -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($m2) { return $m2.FullName }
  return ""
}

function Find-WikiDir([string]$root) {
  $d = Get-ChildItem -Path $root -Recurse -Directory -Filter "Wiki" -ErrorAction SilentlyContinue | Where-Object { $_.FullName -match "\\\\00-.*\\\\Wiki$" } | Select-Object -First 1
  if ($d) { return $d.FullName }
  return ""
}

$result = [ordered]@{
  ok = $false
  task = $task
  started_at = $timestamp
  exit_code = 1
  artifacts = @()
  message = ""
  output = ""
}

try {
  if ($task -eq "wiki_update") {
    $py = Find-File $vaultRoot "generate_wiki.py" "\\wiki_gen\\"
    if (-not $py) { throw "generate_wiki.py not found" }
    $code = Invoke-Exe "python" @($py) $vaultRoot
    if ($code -eq 0) {
      $wikiDir = Find-WikiDir $vaultRoot
      if (-not $wikiDir) { throw "Wiki dir not found" }
      $wikiRel = (Resolve-Path $wikiDir).Path.Substring($vaultRoot.Length).TrimStart("\") -replace "\\", "/"
      $addCode = Invoke-Exe "git" @("add", $wikiRel) $vaultRoot
      if ($addCode -eq 0) {
        $diffCode = Invoke-Exe "git" @("diff", "--cached", "--quiet") $vaultRoot
        if ($diffCode -ne 0) {
          Invoke-Exe "git" @("commit", "-m", "docs(wiki): auto update") $vaultRoot | Out-Null
          $code = Invoke-Exe "git" @("push") $vaultRoot
        }
      }
      if ($addCode -ne 0) { $code = $addCode }
      if ($addCode -eq 0 -and $diffCode -eq 0) { $code = 0 }
      if ($addCode -eq 0 -and $diffCode -ne 0 -and $code -eq 0) { $code = 0 }
    }
    $result.exit_code = $code
    $result.ok = ($code -eq 0)
    $result.message = "wiki_update finished"
    if ($wikiRel) { $result.artifacts += $wikiRel }
    if ($script:lastOutput) { $result.output = ($script:lastOutput -join "`n") }
  }
  elseif ($task -eq "wiki_generate") {
    $py = Find-File $vaultRoot "generate_wiki.py" "\\wiki_gen\\"
    if (-not $py) { throw "generate_wiki.py not found" }
    $code = Invoke-Exe "python" @($py) $vaultRoot
    $result.exit_code = $code
    $result.ok = ($code -eq 0)
    $result.message = "wiki_generate finished"
    $wikiDir = Find-WikiDir $vaultRoot
    if ($wikiDir) {
      $wikiRel = (Resolve-Path $wikiDir).Path.Substring($vaultRoot.Length).TrimStart("\") -replace "\\", "/"
      $result.artifacts += $wikiRel
    }
    if ($script:lastOutput) { $result.output = ($script:lastOutput -join "`n") }
  }
  elseif ($task -eq "git_pull") {
    $code = Invoke-Exe "git" @("pull") $vaultRoot
    $result.exit_code = $code
    $result.ok = ($code -eq 0)
    $result.message = "git_pull finished"
    if ($script:lastOutput) { $result.output = ($script:lastOutput -join "`n") }
  }
  elseif ($task -eq "git_push") {
    $code = Invoke-Exe "git" @("push") $vaultRoot
    $result.exit_code = $code
    $result.ok = ($code -eq 0)
    $result.message = "git_push finished"
    if ($script:lastOutput) { $result.output = ($script:lastOutput -join "`n") }
  }
  elseif ($task -eq "kb_health_check") {
    $py = Find-File $vaultRoot "kb_health_check.py" ""
    if (-not $py) { throw "kb_health_check.py not found" }
    $code = Invoke-Exe "python" @($py) $vaultRoot
    $result.exit_code = $code
    $result.ok = ($code -eq 0)
    $result.message = "kb_health_check finished"
    if ($script:lastOutput) { $result.output = ($script:lastOutput -join "`n") }
  }
  else {
    $result.exit_code = 3
    $result.ok = $false
    $result.message = "unknown task"
  }
}
catch {
  $result.exit_code = 1
  $result.ok = $false
  $result.message = $_.Exception.Message
}

$maxLen = 20000
if ($result.output -and $result.output.Length -gt $maxLen) {
  $result.output = $result.output.Substring(0, $maxLen)
}

$outDir = Join-Path $vaultRoot ".smart-env\\local_worker"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$outPath = Join-Path $outDir ("result_" + (Get-Date -Format "yyyyMMdd_HHmmss") + ".json")
$result | ConvertTo-Json -Depth 5 | Out-File -Encoding UTF8 $outPath

Write-Output $outPath
