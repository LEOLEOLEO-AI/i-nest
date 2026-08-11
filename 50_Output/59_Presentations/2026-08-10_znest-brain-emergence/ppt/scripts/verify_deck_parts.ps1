# Runs the Playwright browser check for all three deck parts.
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $root
try {
  node scripts/check_parts_browser.mjs
  if ($LASTEXITCODE -ne 0) { throw 'browser check failed' }
} finally {
  Pop-Location
}
