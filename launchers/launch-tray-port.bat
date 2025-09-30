@echo off
REM NIA Engineering Portal - Tray Application Launcher with Custom Port (Windows)
REM Usage: launch-tray-port.bat [PORT]
REM Example: launch-tray-port.bat 8080

set CUSTOM_PORT=%1
if "%CUSTOM_PORT%"=="" set CUSTOM_PORT=9091

echo 🚀 NIA Engineering Portal - Background Launcher (Port %CUSTOM_PORT%)
echo ================================================================

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

echo 🖥️  Setting port to %CUSTOM_PORT%...
uv run python -c "from tray_app.config_manager import ConfigManager; cm = ConfigManager(); cm.set('port', %CUSTOM_PORT%); cm.save_config(); print('Port set to %CUSTOM_PORT%')"

echo 🖥️  Launching tray application in background...
echo ✅ You can close this terminal window

REM Launch in background using start command
start /B uv run python tray_app/main.py

echo ✅ Tray application started on port %CUSTOM_PORT%
echo 🖥️  Look for the NIA Engineering Portal icon in your system tray
echo 🛑 To stop the application, right-click the tray icon and select 'Quit'
echo.
echo 💡 Tip: You can also run 'make tray' to start in foreground mode
pause
