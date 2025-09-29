#!/usr/bin/env python3
"""
Build script for the NIA Engineering Portal tray application.
Handles cross-platform executable generation using PyInstaller.
"""

import platform
import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(f"Success: {result.stdout}")
    return True


def build_linux():
    """Build for Linux."""
    print("Building for Linux...")

    # Create dist directory
    dist_dir = Path("dist/linux")
    dist_dir.mkdir(parents=True, exist_ok=True)

    # Build with PyInstaller
    cmd = [
        "uv",
        "run",
        "pyinstaller",
        "--clean",
        "--distpath",
        "dist/linux",
        "tray_app.spec",
    ]

    return run_command(cmd)


def build_windows():
    """Build for Windows (if running on Windows or with Wine)."""
    print("Building for Windows...")

    # Create dist directory
    dist_dir = Path("dist/windows")
    dist_dir.mkdir(parents=True, exist_ok=True)

    # Build with PyInstaller
    cmd = [
        "uv",
        "run",
        "pyinstaller",
        "--clean",
        "--distpath",
        "dist/windows",
        "tray_app.spec",
    ]

    return run_command(cmd)


def build_macos():
    """Build for macOS."""
    print("Building for macOS...")

    # Create dist directory
    dist_dir = Path("dist/macos")
    dist_dir.mkdir(parents=True, exist_ok=True)

    # Build with PyInstaller
    cmd = [
        "uv",
        "run",
        "pyinstaller",
        "--clean",
        "--distpath",
        "dist/macos",
        "tray_app.spec",
    ]

    return run_command(cmd)


def main():
    """Main build function."""
    print("NIA Engineering Portal - Tray Application Build Script")
    print(f"Platform: {platform.system()}")

    # Check if we're in the right directory
    if not Path("tray_app").exists():
        print("Error: tray_app directory not found. Run from project root.")
        sys.exit(1)

    # Check if PyInstaller is available
    try:
        subprocess.run(
            ["uv", "run", "pyinstaller", "--version"], capture_output=True, check=True
        )
    except subprocess.CalledProcessError:
        print("Error: PyInstaller not available. Install with: uv add pyinstaller")
        sys.exit(1)

    # Build for current platform
    current_platform = platform.system().lower()

    if current_platform == "linux":
        success = build_linux()
    elif current_platform == "windows":
        success = build_windows()
    elif current_platform == "darwin":
        success = build_macos()
    else:
        print(f"Unsupported platform: {current_platform}")
        sys.exit(1)

    if success:
        print("Build completed successfully!")
        print(f"Executable created in: dist/{current_platform}/")
    else:
        print("Build failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
