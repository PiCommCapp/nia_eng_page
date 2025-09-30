#!/usr/bin/env python3
"""
Launch script for the NIA Engineering Portal tray application.
Runs the application in the background without keeping the terminal open.
"""

import os
import platform
import subprocess
import sys
from pathlib import Path


def launch_background():
    """Launch the tray application in the background."""
    project_root = Path(__file__).parent.parent

    # Change to project directory
    os.chdir(project_root)

    # Determine the command based on platform
    if platform.system() == "Windows":
        # Windows: Use start command to run in background
        cmd = ["cmd", "/c", "start", "/B", "uv", "run", "python", "tray_app/main.py"]
    else:
        # Unix/Linux/macOS: Use nohup to run in background
        cmd = ["nohup", "uv", "run", "python", "tray_app/main.py", "&"]

    print("🚀 Launching NIA Engineering Portal Tray Application in background...")
    print(f"📍 Command: {' '.join(cmd)}")
    print("✅ Application started - you can close this terminal")

    try:
        if platform.system() == "Windows":
            # Windows: Use subprocess.Popen with creationflags
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            )
        else:
            # Unix/Linux/macOS: Use subprocess.Popen with detach
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                preexec_fn=os.setsid if hasattr(os, "setsid") else None,
            )

        print("✅ Tray application launched successfully!")
        print("🖥️  Look for the NIA Engineering Portal icon in your system tray")
        print("🛑 To stop the application, right-click the tray icon and select 'Quit'")

    except Exception as e:
        print(f"❌ Error launching application: {e}")
        sys.exit(1)


def main():
    """Main entry point."""
    print("NIA Engineering Portal - Background Launcher")
    print("=" * 50)

    # Check if we're in the right directory
    if not Path("tray_app/main.py").exists():
        print("❌ Error: tray_app/main.py not found")
        print("   Please run this script from the project root directory")
        sys.exit(1)

    # Check if UV is available
    try:
        subprocess.run(["uv", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Error: UV not found")
        print("   Please install UV first: https://astral.sh/uv/")
        sys.exit(1)

    launch_background()


if __name__ == "__main__":
    main()
