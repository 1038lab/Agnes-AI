@echo off
cd /d "%~dp0"
echo Starting Agnes Playground...
for /f "tokens=5" %%a in ('netstat -ano ^| find ":8888 " ^| find "LISTENING"') do taskkill /f /pid %%a >nul 2>&1
timeout /t 1 /nobreak >nul
start python server.py
timeout /t 2 /nobreak >nul
start http://localhost:8888
echo Server running at http://localhost:8888
echo Close this window to stop the server
pause
