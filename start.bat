@echo off
echo ========================================
echo   TCC-iNEST Research Platform
echo ========================================
echo.
echo ?????:
echo 1. ????? (????)
echo 2. ????
echo 3. ??????
echo 4. ????
echo 5. ????
echo 6. ??????
echo 7. ???? (Web Dashboard)
echo 8. ????
echo 9. ????
echo 0. ??
echo.
set /p choice=?????:

if "%choice%"=="1" (python main.py --start)
if "%choice%"=="2" (python main.py --paper-scrape)
if "%choice%"=="3" (python main.py --update-kg)
if "%choice%"=="4" (python main.py --generate-insight)
if "%choice%"=="5" (python main.py --sync)
if "%choice%"=="6" (python main.py --report)
if "%choice%"=="7" (start dashboard\index.html)
if "%choice%"=="8" (python scripts\install_skills.py)
if "%choice%"=="9" (pip install -r requirements.txt)

pause
