@echo off
setlocal
chcp 65001 >nul 2>&1

python "%~dp0generate_wiki.py"

endlocal
