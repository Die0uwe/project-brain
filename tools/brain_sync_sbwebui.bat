@echo off
rem Zet Project Brain in de Bibliotheek van SBWebUI (categorie "DieOuwe Brain"). Eerst een droogloop, dan de vraag of het echt mag.
rem Resultaat ook in %USERPROFILE%\brain-sync-sbwebui.log. Voor de Taakplanner: brain_sync_sbwebui.bat /auto (zonder vragen).
chcp 65001 >nul
cd /d "%~dp0.."
set PYTHONUTF8=1
if /i "%~1"=="/auto" (
  echo ==== %DATE% %TIME% ==== >> "%USERPROFILE%\brain-sync-sbwebui.log"
  python tools\brain_sync_sbwebui.py >> "%USERPROFILE%\brain-sync-sbwebui.log" 2>&1
  exit /b %ERRORLEVEL%
)
python tools\brain_sync_sbwebui.py --dry-run
if errorlevel 1 ( echo. & echo Droogloop mislukt; er is niets veranderd. & pause & exit /b 1 )
echo.
choice /m "Nu echt bijwerken in SBWebUI"
if errorlevel 2 exit /b 0
python tools\brain_sync_sbwebui.py --no-pull
echo.
pause
