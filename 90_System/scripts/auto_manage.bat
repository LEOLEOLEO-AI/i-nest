@echo off
REM Obsidian Knowledge Base Auto-Management Runner
REM Called by Windows Task Scheduler

set VAULT_ROOT=D:\Obsidian\home\work\.openclaw\workspace
set PYTHON=%VAULT_ROOT%\.venv\Scripts\python.exe
set SCRIPT=%VAULT_ROOT%\90_System\scripts\reorganize.py
set LOG_DIR=%VAULT_ROOT%\90_System\logs

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

cd /d "%VAULT_ROOT%"

echo ======================================== >> "%LOG_DIR%\auto_manage.log"
echo [%date% %time%] Starting auto-management... >> "%LOG_DIR%\auto_manage.log"

REM Process inbox notes
"%PYTHON%" "%SCRIPT%" --process-inbox --batch-size 3 >> "%LOG_DIR%\auto_manage.log" 2>&1

REM Auto-commit changes via git
git add -A >> "%LOG_DIR%\auto_manage.log" 2>&1
git commit -m "auto: inbox processing %date% %time%" >> "%LOG_DIR%\auto_manage.log" 2>&1

echo [%date% %time%] Auto-management complete. >> "%LOG_DIR%\auto_manage.log"
