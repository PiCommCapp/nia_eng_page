#!/usr/bin/env python3
"""
Create desktop shortcut for the NIA Engineering Portal tray application.
This script creates platform-specific shortcuts that launch the app in background.
"""

import os
import platform
import subprocess
from pathlib import Path


def create_desktop_shortcut():
    """Create a desktop shortcut for the tray application."""
    project_root = Path(__file__).parent.parent
    app_name = "NIA Engineering Portal"

    if platform.system() == "Windows":
        create_windows_shortcut(project_root, app_name)
    elif platform.system() == "Darwin":  # macOS
        create_macos_shortcut(project_root, app_name)
    else:  # Linux
        create_linux_shortcut(project_root, app_name)


def create_windows_shortcut(project_root, app_name):
    """Create Windows shortcut."""
    desktop = Path.home() / "Desktop"
    shortcut_path = desktop / f"{app_name}.bat"

    shortcut_content = f'''@echo off
cd /d "{project_root}"
start /B uv run python tray_app/main.py
echo {app_name} started in background
echo You can close this window
pause
'''

    with open(shortcut_path, "w") as f:
        f.write(shortcut_content)

    print(f"✅ Windows shortcut created: {shortcut_path}")
    print("🖥️  Double-click the shortcut to launch the application")


def create_macos_shortcut(project_root, app_name):
    """Create macOS application bundle."""
    app_dir = Path.home() / "Applications" / f"{app_name}.app"
    contents_dir = app_dir / "Contents"
    macos_dir = contents_dir / "MacOS"

    # Create directory structure
    macos_dir.mkdir(parents=True, exist_ok=True)

    # Create Info.plist
    info_plist = contents_dir / "Info.plist"
    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>launch.sh</string>
    <key>CFBundleIdentifier</key>
    <string>com.nia.engineering-portal</string>
    <key>CFBundleName</key>
    <string>{app_name}</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
</dict>
</plist>"""

    with open(info_plist, "w") as f:
        f.write(plist_content)

    # Create launch script
    launch_script = macos_dir / "launch.sh"
    script_content = f'''#!/bin/bash
cd "{project_root}"
nohup uv run python tray_app/main.py > /dev/null 2>&1 &
'''

    with open(launch_script, "w") as f:
        f.write(script_content)

    # Make script executable
    os.chmod(launch_script, 0o744)

    print(f"✅ macOS application created: {app_dir}")
    print("🖥️  You can find the app in your Applications folder")


def create_linux_shortcut(project_root, app_name):
    """Create Linux desktop entry."""
    desktop_dir = Path.home() / ".local" / "share" / "applications"
    desktop_dir.mkdir(parents=True, exist_ok=True)

    desktop_entry = desktop_dir / f"{app_name.lower().replace(' ', '-')}.desktop"

    entry_content = f'''[Desktop Entry]
Version=1.0
Type=Application
Name={app_name}
Comment=NIA Engineering Portal Tray Application
Exec=cd "{project_root}" && nohup uv run python tray_app/main.py > /dev/null 2>&1 &
Icon=applications-utilities
Terminal=false
StartupNotify=false
Categories=Utility;Network;
'''

    with open(desktop_entry, "w") as f:
        f.write(entry_content)

    # Make executable
    os.chmod(desktop_entry, 0o744)

    print(f"✅ Linux desktop entry created: {desktop_entry}")
    print("🖥️  You can find the application in your applications menu")


def main():
    """Main entry point."""
    print("🚀 Creating desktop shortcut for NIA Engineering Portal")
    print("=" * 60)

    # Check if we're in the right directory
    if not Path("tray_app/main.py").exists():
        print("❌ Error: tray_app/main.py not found")
        print("   Please run this script from the project root directory")
        return

    # Check if UV is available
    try:
        subprocess.run(["uv", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Error: UV not found")
        print("   Please install UV first: https://astral.sh/uv/")
        return

    create_desktop_shortcut()
    print("\n✅ Desktop shortcut creation complete!")


if __name__ == "__main__":
    main()
