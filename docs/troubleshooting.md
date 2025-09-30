# NIA Engineering Portal - Troubleshooting Guide

## 🚨 Quick Diagnosis

### Check Application Status

```bash
# Check system status
make status

# Check if server is running
make kill  # This will show if anything was running

# Check logs
tail -f nia_tray_app.log
```

### Common Quick Fixes

1. **Restart Application**: `make kill && make tray-bg`
2. **Reinstall Dependencies**: `make install`
3. **Check Port**: Ensure port 9001 is available
4. **Check Logs**: Look for error messages in `nia_tray_app.log`

## 🔍 Detailed Troubleshooting

### Application Won't Start

#### Symptoms

- Tray icon doesn't appear
- Error messages when running `make tray-bg`
- Application exits immediately

#### Diagnosis Steps

1. **Check Dependencies**:

   ```bash
   make status
   uv run python --version
   ```

2. **Check Logs**:

   ```bash
   tail -20 nia_tray_app.log
   ```

3. **Check Port Availability**:

   ```bash
   # Unix/Linux/macOS
   lsof -i :9001

   # Windows
   netstat -an | findstr 9001
   ```

#### Solutions

- **Missing Dependencies**: Run `make install`
- **Port in Use**: Kill the process using port 9001 or change port in config
- **Python Issues**: Reinstall Python 3.12+ or use UV to manage Python
- **Permission Issues**: Check file permissions and run with appropriate privileges

### Tray Icon Not Visible

#### Symptoms

- Application appears to start but no tray icon
- Process is running but no system tray icon

#### Diagnosis Steps

1. **Check Process**:

   ```bash
   # Unix/Linux/macOS
   ps aux | grep python

   # Windows
   tasklist | findstr python
   ```

2. **Check System Tray**:

   - Look in system tray area
   - Check if tray is hidden or collapsed
   - Try different desktop environments (Linux)

3. **Check Logs**:
   ```bash
   grep -i "tray\|icon" nia_tray_app.log
   ```

#### Solutions

- **System Tray Issues**: Restart desktop environment or system
- **Icon Hidden**: Check system tray settings to show all icons
- **Permission Issues**: Run with appropriate privileges
- **Desktop Environment**: Some Linux desktop environments don't support system tray

### Portal Won't Load

#### Symptoms

- Tray icon is visible but clicking doesn't open portal
- Browser shows "This site can't be reached" or similar error
- Portal loads but shows errors

#### Diagnosis Steps

1. **Check Server Status**:

   - Tray icon should be green (running)
   - Check if server is actually running

2. **Check URL**:

   - Try accessing `http://localhost:9001` directly
   - Check if port is correct in configuration

3. **Check Browser**:

   - Try different browser
   - Check browser console for errors
   - Disable browser extensions temporarily

4. **Check Firewall**:
   - Ensure localhost connections are allowed
   - Check if antivirus is blocking the connection

#### Solutions

- **Server Not Running**: Restart application or start server manually
- **Wrong Port**: Check configuration and update if needed
- **Browser Issues**: Try different browser or clear browser cache
- **Firewall Issues**: Add exception for localhost connections

### Configuration Issues

#### Symptoms

- Configuration dialog won't open
- Settings don't save
- Application uses wrong settings

#### Diagnosis Steps

1. **Check Configuration File**:

   ```bash
   cat tray_app/config.json
   ```

2. **Check File Permissions**:

   ```bash
   ls -la tray_app/config.json
   ```

3. **Check JSON Format**:
   ```bash
   python -m json.tool tray_app/config.json
   ```

#### Solutions

- **Invalid JSON**: Fix JSON syntax or delete file to reset
- **Permission Issues**: Fix file permissions
- **Corrupted Config**: Delete config file to reset to defaults
- **Missing Config**: Create default configuration

### Performance Issues

#### Symptoms

- Application starts slowly
- Portal loads slowly
- High CPU or memory usage

#### Diagnosis Steps

1. **Check Resource Usage**:

   ```bash
   # Unix/Linux/macOS
   top -p $(pgrep -f "python.*tray_app")

   # Windows
   tasklist /fi "imagename eq python.exe"
   ```

2. **Check Logs for Errors**:

   ```bash
   grep -i "error\|warning" nia_tray_app.log
   ```

3. **Check System Resources**:
   - Available memory
   - CPU usage
   - Disk space

#### Solutions

- **High Memory Usage**: Restart application periodically
- **Slow Startup**: Check for large log files or configuration issues
- **High CPU Usage**: Check for infinite loops or resource leaks
- **System Resources**: Ensure adequate system resources

## 🛠️ Advanced Troubleshooting

### Debug Mode

Enable debug logging for more detailed information:

1. **Edit Configuration**:

   ```json
   {
     "log_level": "DEBUG"
   }
   ```

2. **Restart Application**:

   ```bash
   make kill
   make tray-bg
   ```

3. **Check Debug Logs**:
   ```bash
   tail -f nia_tray_app.log
   ```

### Manual Testing

Test individual components:

```bash
# Test configuration manager
uv run python -c "from tray_app.config_manager import ConfigManager; cm = ConfigManager(); print('Config manager OK')"

# Test server controller
uv run python -c "from tray_app.server_controller import ServerController; from tray_app.config_manager import ConfigManager; cm = ConfigManager(); sc = ServerController(cm); print('Server controller OK')"

# Test GUI components
uv run python -c "from tray_app.gui_components import ConfigurationDialog; print('GUI components OK')"
```

### Reset to Defaults

If all else fails, reset to default configuration:

```bash
# Stop application
make kill

# Remove configuration
rm tray_app/config.json

# Remove logs
rm nia_tray_app.log

# Restart application
make tray-bg
```

## 📋 Platform-Specific Issues

### Windows Issues

#### Common Problems

- **PowerShell Execution Policy**: May block script execution
- **Antivirus Software**: May block application or connections
- **User Account Control**: May require administrator privileges

#### Solutions

- **Execution Policy**: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- **Antivirus**: Add exception for application directory
- **UAC**: Run PowerShell as Administrator when installing

### macOS Issues

#### Common Problems

- **Gatekeeper**: May block unsigned applications
- **Python Version**: System Python may be outdated
- **Permission Issues**: May need to grant accessibility permissions

#### Solutions

- **Gatekeeper**: Allow application in System Preferences > Security & Privacy
- **Python**: Use UV to manage Python versions
- **Permissions**: Grant necessary permissions when prompted

### Linux Issues

#### Common Problems

- **Desktop Environment**: Some environments don't support system tray
- **Python Dependencies**: May need additional system packages
- **Permission Issues**: May need to install additional packages

#### Solutions

- **Desktop Environment**: Use supported environment (GNOME, KDE, XFCE)
- **Dependencies**: Install required system packages
- **Permissions**: Check file permissions and ownership

## 📞 Getting Help

### Before Asking for Help

1. **Check This Guide**: Review all relevant sections
2. **Check Logs**: Look at `nia_tray_app.log` for error messages
3. **Check Status**: Run `make status` to verify system state
4. **Try Solutions**: Attempt the suggested solutions
5. **Document Issue**: Note exact steps to reproduce the problem

### Information to Provide

When reporting issues, include:

1. **Operating System**: Version and architecture
2. **Python Version**: Output of `python --version`
3. **Error Messages**: Complete error messages from logs
4. **Steps to Reproduce**: Exact steps that caused the issue
5. **System Status**: Output of `make status`
6. **Log Files**: Relevant portions of `nia_tray_app.log`

### Self-Service Resources

- **User Guide**: `docs/user-guide.md`
- **Installation Guide**: `docs/installation.md`
- **Technical Documentation**: `docs/technical.md`
- **Project Status**: `docs/tasks.md`

## 🔄 Prevention

### Regular Maintenance

1. **Check Logs**: Regularly review log files for issues
2. **Update Dependencies**: Keep dependencies up to date
3. **Monitor Resources**: Watch for resource usage issues
4. **Test Functionality**: Periodically test all features

### Best Practices

1. **Backup Configuration**: Keep backups of working configurations
2. **Document Changes**: Note any custom configurations
3. **Test Updates**: Test updates in a safe environment first
4. **Monitor System**: Keep an eye on system resources

---

## 📊 Troubleshooting Checklist

### Before Reporting Issues

- [ ] Checked this troubleshooting guide
- [ ] Checked application logs
- [ ] Verified system status
- [ ] Tried restarting application
- [ ] Tried reinstalling dependencies
- [ ] Checked system resources
- [ ] Verified network connectivity
- [ ] Tested with different browser
- [ ] Checked file permissions
- [ ] Documented exact error messages

### Information Collected

- [ ] Operating system and version
- [ ] Python version
- [ ] Application version
- [ ] Error messages
- [ ] Steps to reproduce
- [ ] System status output
- [ ] Log file contents
- [ ] Configuration file contents

---

_Last Updated: December 2024_
_Version: 1.0.0_
_Status: Production Ready_
