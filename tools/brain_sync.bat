@echo off
rem Synchroniseert project-brain naar Open WebUI en schrijft het resultaat naar %USERPROFILE%\brain-sync.log
rem Voor de Windows-taakplanner: wijs de taak naar dit bestand. Instellingen staan in %USERPROFILE%\.openwebui-brain.env
cd /d "%~dp0.."
echo ==== %DATE% %TIME% ==== >> "%USERPROFILE%\brain-sync.log"
python tools\openwebui_sync.py >> "%USERPROFILE%\brain-sync.log" 2>&1
exit /b %ERRORLEVEL%
