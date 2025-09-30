#!/bin/bash
# NIA Engineering Portal - Tray Application Launcher (Unix/Linux/macOS)
# This script launches the tray application in the background

echo "🚀 NIA Engineering Portal - Background Launcher"
echo "=============================================="

# Check if we're in the right directory
if [ ! -f "tray_app/main.py" ]; then
    echo "❌ Error: tray_app/main.py not found"
    echo "   Please run this script from the project root directory"
    exit 1
fi

# Check if UV is available
if ! command -v uv &> /dev/null; then
    echo "❌ Error: UV not found"
    echo "   Please install UV first: https://astral.sh/uv/"
    exit 1
fi

echo "🖥️  Launching tray application in background..."
echo "✅ You can close this terminal window"

# Launch in background with nohup
nohup uv run python tray_app/main.py > /dev/null 2>&1 &

# Get the process ID
PID=$!

echo "✅ Tray application started (PID: $PID)"
echo "🖥️  Look for the NIA Engineering Portal icon in your system tray"
echo "🛑 To stop the application, right-click the tray icon and select 'Quit'"
echo ""
echo "💡 Tip: You can also run 'make tray' to start in foreground mode"
