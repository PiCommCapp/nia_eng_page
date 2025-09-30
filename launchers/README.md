# NIA Engineering Portal - Launchers

This folder contains various launcher scripts for the NIA Engineering Portal tray application.

## Available Launchers

### Platform-Specific Scripts

- **`launch-tray.sh`** - Unix/Linux/macOS launcher script
- **`launch-tray.bat`** - Windows launcher script

### Python Launcher

- **`../scripts/launch_tray.py`** - Cross-platform Python launcher

## Usage

### Quick Launch (Recommended)

Use the makefile commands for the easiest experience:

```bash
# Launch in background (no terminal needed)
make tray-bg

# Create desktop shortcut
make tray-shortcut
```

### Manual Launch

#### Unix/Linux/macOS

```bash
# Make executable (first time only)
chmod +x launchers/launch-tray.sh

# Launch the application
./launchers/launch-tray.sh
```

#### Windows

```cmd
# Launch the application
launchers\launch-tray.bat
```

#### Cross-Platform Python

```bash
# Launch using Python script
uv run python scripts/launch_tray.py
```

## Features

All launchers provide:

- ✅ **Background execution** - No need to keep terminal open
- ✅ **Cross-platform support** - Works on Windows, macOS, and Linux
- ✅ **Error checking** - Validates environment before launching
- ✅ **User feedback** - Clear messages about application status
- ✅ **Easy termination** - Right-click tray icon to quit

## Desktop Shortcuts

The `make tray-shortcut` command creates platform-specific desktop shortcuts:

- **Windows**: Creates a `.bat` file on the desktop
- **macOS**: Creates an `.app` bundle in Applications folder
- **Linux**: Creates a `.desktop` entry in applications menu

## Troubleshooting

### Common Issues

1. **"UV not found" error**

   - Install UV: https://astral.sh/uv/
   - Or use the Python launcher: `python scripts/launch_tray.py`

2. **"tray_app/main.py not found" error**

   - Make sure you're running from the project root directory
   - Check that the project structure is intact

3. **Application doesn't start**
   - Check if another instance is already running
   - Look for the tray icon in your system tray
   - Check the log file: `nia_tray_app.log`

### Getting Help

- Check the main project README for setup instructions
- Review the makefile help: `make help`
- Check the application logs for detailed error messages

## File Structure

```
launchers/
├── README.md           # This file
├── launch-tray.sh      # Unix/Linux/macOS launcher
└── launch-tray.bat     # Windows launcher

scripts/
└── launch_tray.py      # Cross-platform Python launcher
```
