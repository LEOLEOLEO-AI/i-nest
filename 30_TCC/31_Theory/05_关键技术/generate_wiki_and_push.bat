@echo off
setlocal
chcp 65001 >nul 2>&1

call "%~dp0generate_wiki.bat"
if %errorlevel% neq 0 exit /b %errorlevel%

git add "00-索引\Wiki" 1>nul 2>nul

git diff --cached --quiet
if %errorlevel% equ 0 (
  echo No wiki changes.
  exit /b 0
)

git commit -m "docs(wiki): auto update" 1>nul
git push 1>nul

endlocal
