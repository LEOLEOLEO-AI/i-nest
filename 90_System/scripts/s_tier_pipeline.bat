@echo off
chcp 65001 >nul
echo ============================================
echo   S-TIER AUTOMATION PIPELINE
echo   %date% %time%
echo ============================================

set PYTHON=C:\Users\LEO\AppData\Local\Programs\Python\Python310\python.exe
set VAULT=D:\Obsidian\home\work\.openclaw\workspace
set SCRIPTS=%VAULT%\90_System\scripts
set LOG=%VAULT%\logs\pipeline_%date:~0,10%.log

echo [1/6] Unified Data Bus...
%PYTHON% -X utf8 "%SCRIPTS%\unified_data_bus.py" >> "%LOG%" 2>&1

echo [2/6] Process Inbox...
%PYTHON% -X utf8 "%SCRIPTS%\process_inbox.py" >> "%LOG%" 2>&1

echo [3/6] Process 20_Processing...
%PYTHON% -X utf8 "%SCRIPTS%\processing_workflow.py" >> "%LOG%" 2>&1

echo [4/6] Daily Insights...
%PYTHON% -X utf8 "%SCRIPTS%\daily_insights.py" >> "%LOG%" 2>&1

echo [5/6] Task Board...
%PYTHON% -X utf8 "%SCRIPTS%\task_board.py" >> "%LOG%" 2>&1

echo [6/6] Git Sync...
cd /d "%VAULT%"
git add -A >> "%LOG%" 2>&1
git commit -m "auto: S-tier pipeline %date%" >> "%LOG%" 2>&1
git push >> "%LOG%" 2>&1

echo Done: %date% %time% >> "%LOG%"
echo ============================================
echo   PIPELINE COMPLETE
echo ============================================
