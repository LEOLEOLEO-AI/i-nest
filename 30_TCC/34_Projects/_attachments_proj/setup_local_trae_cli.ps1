param(
  [string]$TraeExePath = ""
)

$ErrorActionPreference = "Stop"

function Find-TraeExe {
  $candidates = @(
    "$Env:LOCALAPPDATA\\Programs\\Trae\\Trae.exe",
    "$Env:ProgramFiles\\Trae\\Trae.exe",
    "$Env:ProgramFiles(x86)\\Trae\\Trae.exe"
  )
  foreach ($c in $candidates) {
    if (Test-Path $c) { return $c }
  }
  return ""
}

if (-not $TraeExePath) {
  $TraeExePath = Find-TraeExe
}

if (-not $TraeExePath -or -not (Test-Path $TraeExePath)) {
  Write-Host "ERROR: Trae.exe not found. Re-run with -TraeExePath <full path>." -ForegroundColor Red
  exit 1
}

$binDir = Join-Path $Env:USERPROFILE ".local\\bin"
New-Item -ItemType Directory -Force -Path $binDir | Out-Null

$shim = Join-Path $binDir "trae.cmd"
$content = "@echo off`r`nstart \"\" `"$TraeExePath`"`r`n"
Set-Content -Path $shim -Value $content -Encoding ASCII

$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if (-not ($userPath -split ";" | Where-Object { $_ -eq $binDir })) {
  [Environment]::SetEnvironmentVariable("Path", ($userPath + ";" + $binDir), "User")
}

Write-Host "OK: Created shim: $shim" -ForegroundColor Green
Write-Host "NOTE: Open a new terminal to use 'trae' from PATH." -ForegroundColor Yellow
