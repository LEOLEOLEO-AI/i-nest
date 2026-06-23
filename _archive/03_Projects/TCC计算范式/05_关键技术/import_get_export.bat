@echo off
setlocal
chcp 65001 >nul 2>&1

if "%~1"=="" (
  echo Usage: import_get_export.bat ^<GetExportFolderOrZip^>
  echo Example: import_get_export.bat "C:\Users\%USERNAME%\Downloads\get_export.zip"
  exit /b 2
)

python "%~dp0import_get_export.py" "%~1" --download-remote-images

endlocal
