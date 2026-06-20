param(
  [Parameter(Mandatory = $true)][string]$CloudHost,
  [Parameter(Mandatory = $true)][string]$CloudUser,
  [int]$CloudPort = 22,
  [int]$LocalSshPort = 22,
  [int]$ReversePort = 2222
)

$ErrorActionPreference = "Stop"

$ssh = Get-Command ssh -ErrorAction SilentlyContinue
if (-not $ssh) {
  Write-Host "ERROR: ssh client not found. Install OpenSSH Client." -ForegroundColor Red
  exit 1
}

$args = @(
  "-N",
  "-p", "$CloudPort",
  "-R", "$ReversePort`:localhost`:$LocalSshPort",
  "-o", "ServerAliveInterval=30",
  "-o", "ServerAliveCountMax=3",
  "-o", "ExitOnForwardFailure=yes",
  "$CloudUser@$CloudHost"
)

Write-Host "Starting reverse tunnel: $CloudHost:$ReversePort -> localhost:$LocalSshPort" -ForegroundColor Cyan
Start-Process -FilePath $ssh.Source -ArgumentList $args -WindowStyle Hidden
Write-Host "OK: reverse tunnel process started." -ForegroundColor Green
