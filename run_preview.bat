@echo off
title HudIsThinking - Preview Server
cd /d "%~dp0"

echo ===============================================================
echo               HUDISTHINKING LLC - LOCAL PREVIEW
echo ===============================================================
echo.

if not exist "venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found in venv\
    echo Please make sure the venv directory exists.
    pause
    exit /b 1
)

echo [*] Starting Django Preview Server at http://127.0.0.1:8000/
echo [*] Admin Dashboard: http://127.0.0.1:8000/admin/
echo [*] Press Ctrl+C at any time to stop the server.
echo.

:: Automatically open default browser after a 2-second delay in background
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:8000/"

:: Launch Django server
venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] Server stopped or encountered an error.
    pause
)
