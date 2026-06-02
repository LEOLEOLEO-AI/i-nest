@echo off
REM Weekly full reorganization of Obsidian knowledge base

set VAULT_ROOT=D:\Obsidian\home\work\.openclaw\workspace
set PYTHON=%VAULT_ROOT%\.venv\Scripts\python.exe
set SCRIPT=%VAULT_ROOT%\90_System\scripts\reorganize.py
set LOG_DIR=%VAULT_ROOT%\90_System\logs

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

cd /d "%VAULT_ROOT%"

echo ======================================== >> "%LOG_DIR%\weekly_reorg.log"
echo [%date% %time%] Starting weekly full reorganization... >> "%LOG_DIR%\weekly_reorg.log"

REM Full reorganization (skip embeddings for speed)
"%PYTHON%" "%SCRIPT%" --batch-size 3 >> "%LOG_DIR%\weekly_reorg.log" 2>&1

REM Commit changes
git add -A >> "%LOG_DIR%\weekly_reorg.log" 2>&1
git commit -m "auto: weekly full reorganization %date%" >> "%LOG_DIR%\weekly_reorg.log" 2>&1

echo [%date% %time%] Weekly reorganization complete. >> "%LOG_DIR%\weekly_reorg.log"
