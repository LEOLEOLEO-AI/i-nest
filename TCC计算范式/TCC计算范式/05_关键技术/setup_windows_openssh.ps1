$ErrorActionPreference = "Stop"

$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
  Write-Host "ERROR: Run this script as Administrator." -ForegroundColor Red
  exit 1
}

$cap = Get-WindowsCapability -Online | Where-Object { $_.Name -like "OpenSSH.Server*" }
if ($cap.State -ne "Installed") {
  Add-WindowsCapability -Online -Name $cap.Name | Out-Null
}

Set-Service -Name "sshd" -StartupType Automatic
Start-Service -Name "sshd"

if (-not (Get-NetFirewallRule -Name "OpenSSH-Server-In-TCP" -ErrorAction SilentlyContinue)) {
  New-NetFirewallRule -Name "OpenSSH-Server-In-TCP" -DisplayName "OpenSSH Server (sshd)" -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22 | Out-Null
}

Get-Service sshd | Format-Table Status, Name, StartType
Write-Host "OK: OpenSSH server is enabled." -ForegroundColor Green
