# NIA Engineering Portal - User Guide

## 🚀 Quick Start

### For New Users (5 Minutes to Running)

1. **Install Dependencies**:

   ```bash
   make install
   ```

2. **Launch Application**:

   ```bash
   make tray-bg
   ```

   _This launches the app in background - you can close the terminal_

3. **Access Portal**:

   - Look for the NIA Engineering Portal icon in your system tray
   - Click the icon to open the portal
   - The portal will open in your default web browser

4. **Create Desktop Shortcut** (Optional):
   ```bash
   make tray-shortcut
   ```

## 🖥️ Using the Desktop Tray Application

### System Tray Icon

The application runs as a system tray icon with the following states:

- **Green Icon**: Server is running and portal is accessible
- **Gray Icon**: Server is stopped
- **Red Icon**: Error state

### Tray Menu Options

Right-click the tray icon to access:

- **Open Portal**: Launch the web portal in your browser
- **Configure**: Open configuration dialog
- **Start Server**: Start the HTTP server
- **Stop Server**: Stop the HTTP server
- **Quit**: Exit the application

### Configuration

1. Right-click the tray icon
2. Select "Configure"
3. A web-based configuration page will open
4. Adjust settings as needed
5. Click "Save" to apply changes

## 🌐 Using the Web Portal

### Navigation Structure

The portal is organized hierarchically:

1. **Main Page**: Overview of all available systems
2. **Committee Rooms**: Access to specific committee rooms
3. **Role Selection**: Choose Engineer or Operator role
4. **System Access**: Direct links to all engineering systems

### Committee Room Access

1. Click "Committee Rooms" on the main page
2. Select your committee room (CR21, CR29, CR30, Senate)
3. Choose your role (Engineer or Operator)
4. Access all systems for your role

### System Categories

- **KVM Switches**: AIM Main/Reserve access
- **Network Infrastructure**: Firewalls, Dante audio, control systems
- **Control Rooms**: CAR2, B23 committee rooms
- **Gallery Screens**: PDU management interfaces
- **Support Systems**: Busby admin, documentation

## 🔧 Troubleshooting

### Common Issues

#### Application Won't Start

- **Check Dependencies**: Run `make install` to ensure all dependencies are installed
- **Check Port**: Make sure port 9001 is not in use by another application
- **Check Logs**: Look at `nia_tray_app.log` for error messages

#### Tray Icon Not Visible

- **Check System Tray**: Look for the icon in your system tray area
- **Check Task Manager**: Verify the process is running
- **Restart Application**: Stop and restart the application

#### Portal Won't Load

- **Check Server Status**: Ensure the server is running (green tray icon)
- **Check URL**: Make sure you're accessing `http://localhost:9001`
- **Check Browser**: Try a different web browser
- **Check Firewall**: Ensure localhost connections are allowed

#### Configuration Issues

- **Check File Permissions**: Ensure the application can write to the config file
- **Check JSON Format**: Verify the configuration file is valid JSON
- **Reset Configuration**: Delete the config file to reset to defaults

### Getting Help

1. **Check Logs**: Look at `nia_tray_app.log` for detailed error messages
2. **Check Documentation**: Review this user guide and troubleshooting section
3. **Check Status**: Run `make status` to check system status
4. **Restart Application**: Try stopping and restarting the application

## 📱 Platform-Specific Instructions

### Windows

- **Installation**: Use `make install` or install UV manually
- **Launch**: Use `make tray-bg` or double-click `launchers\launch-tray.bat`
- **Tray Icon**: Look in the system tray (bottom-right corner)
- **Desktop Shortcut**: Created on Desktop when using `make tray-shortcut`

### macOS

- **Installation**: Use `make install` or install UV manually
- **Launch**: Use `make tray-bg` or run `./launchers/launch-tray.sh`
- **Tray Icon**: Look in the menu bar (top-right corner)
- **Desktop Shortcut**: Created in Applications folder when using `make tray-shortcut`

### Linux

- **Installation**: Use `make install` or install UV manually
- **Launch**: Use `make tray-bg` or run `./launchers/launch-tray.sh`
- **Tray Icon**: Look in the system tray (varies by desktop environment)
- **Desktop Shortcut**: Created in applications menu when using `make tray-shortcut`

## 🔄 Maintenance

### Regular Tasks

- **Check Updates**: Regularly check for application updates
- **Monitor Logs**: Review log files for any issues
- **Test Functionality**: Periodically test all portal functions
- **Backup Configuration**: Keep backups of your configuration

### Updating the Application

1. **Stop Application**: Right-click tray icon and select "Quit"
2. **Update Code**: Pull latest changes from repository
3. **Update Dependencies**: Run `make update`
4. **Restart Application**: Run `make tray-bg`

### Configuration Backup

- **Location**: `tray_app/config.json`
- **Backup**: Copy this file to a safe location
- **Restore**: Replace the file to restore configuration

## 📞 Support

### Self-Service

1. **Check This Guide**: Review all sections thoroughly
2. **Check Logs**: Look at `nia_tray_app.log` for error details
3. **Check Status**: Run `make status` to verify system state
4. **Restart Application**: Try stopping and restarting

### Getting Additional Help

- **Documentation**: Check `docs/` folder for technical documentation
- **Logs**: Provide log file contents when reporting issues
- **System Info**: Include your operating system and version
- **Steps to Reproduce**: Describe exactly what you did before the issue occurred

---

## 🎯 Quick Reference

### Essential Commands

```bash
make install          # Install dependencies
make tray-bg          # Launch in background
make tray-shortcut    # Create desktop shortcut
make status           # Check system status
make help             # Show all available commands
```

### Key Files

- **Application**: `tray_app/main.py`
- **Configuration**: `tray_app/config.json`
- **Logs**: `nia_tray_app.log`
- **Portal**: `pages/index.html`

### Default Settings

- **Port**: 9001
- **URL**: http://localhost:9001
- **Configuration**: Web-based interface
- **Logging**: File and console output

---

_Last Updated: December 2024_
_Version: 1.0.0_
_Status: Production Ready_
