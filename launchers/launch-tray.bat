@echo off
REM NIA Engineering Portal - Tray Application Launcher (Windows)
REM This script launches the tray application in the background

echo 🚀 NIA Engineering Portal - Background Launcher
echo ==============================================

REM Check if we're in the right directory
if not exist "tray_app\main.py" (
    echo ❌ Error: tray_app\main.py not found
    echo    Please run this script from the project root directory
    pause
    exit /b 1
)

REM Check if UV is available
uv --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: UV not found
    echo    Please install UV first: https://astral.sh/uv/
    pause
    exit /b 1
)

echo 🖥️  Launching tray application in background...
echo ✅ You can close this terminal window

REM Launch in background using start command
start /B uv run python tray_app/main.py

echo ✅ Tray application started
echo 🖥️  Look for the NIA Engineering Portal icon in your system tray
echo 🛑 To stop the application, right-click the tray icon and select 'Quit'
echo.
echo 💡 Tip: You can also run 'make tray' to start in foreground mode
pause
