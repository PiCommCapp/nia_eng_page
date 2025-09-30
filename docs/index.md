# NIA Engineering Portal

A lightning-fast, mission-critical engineering portal for broadcast/AV infrastructure access with desktop tray application support.

## 🚀 Quick Start

Get up and running in 5 minutes:

1. **Install Dependencies**: `make install`
2. **Launch Application**: `make tray-bg` (runs in background)
3. **Access Portal**: Click the tray icon or use desktop shortcut
4. **Create Shortcut**: `make tray-shortcut` (optional)

## ✨ Features

- **🖥️ Desktop Tray Application**: Cross-platform system tray integration (Windows, macOS, Linux)
- **⚙️ Web-based Configuration**: Easy management through web interface
- **⚡ Instant Access**: Static HTML interface loads immediately
- **🧭 Intuitive Navigation**: Clean categorization of all systems
- **📱 Local Deployment**: Works offline, no external dependencies
- **🔄 Background Operation**: Runs without keeping terminal open
- **🎯 Zero Training**: Engineers can use it immediately

## 📚 Documentation

### For Users

- **[Installation Guide](installation.md)** - Step-by-step setup instructions
- **[User Guide](user-guide.md)** - Complete user manual
- **[Troubleshooting](troubleshooting.md)** - Problem-solving guide

### For Developers

- **[Technical Architecture](technical.md)** - System design and implementation
- **[Deployment Guide](deployment.md)** - Production deployment procedures
- **[Testing Documentation](testing.md)** - Testing framework and procedures
- **[Page Structure](pages.md)** - Web page organization and structure

### Project Information

- **[Project Tasks](tasks.md)** - Current status and task tracking
- **[Project Context](context.md)** - Project background and user scenarios
- **[Project Brief](projectbrief.md)** - Project overview and requirements
- **[Environment Setup](environment.md)** - Development environment configuration

## 🏗️ Architecture

### Current Implementation

- **Desktop Tray Application**: Cross-platform system tray integration
- **Web-based Configuration**: Easy management through web interface
- **Static HTML Interface**: Fast-loading web pages
- **Local File Deployment**: Works offline, no external dependencies
- **Background Operation**: Runs without keeping terminal open

### Technical Stack

- **Backend**: Python 3.12+ with HTTP server
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Desktop**: PyInstaller, pystray for cross-platform tray application
- **Configuration**: JSON-based configuration management
- **Testing**: pytest with comprehensive test coverage
- **Build**: UV package manager, cross-platform makefile
- **CI/CD**: GitHub Actions for automated builds and releases

## 🎯 System Categories

- **KVM Switches**: AIM Main/Reserve access
- **Network Infrastructure**: Firewalls, Dante audio, control systems
- **Control Rooms**: CAR2, B23 committee rooms
- **Gallery Screens**: PDU management interfaces
- **Support Systems**: Busby admin, documentation

## 🚀 Launch Options

### Desktop Tray Application (Recommended)

```bash
make tray-bg          # Launch in background
make tray-shortcut    # Create desktop shortcut
```

### Manual Launch

```bash
# Unix/Linux/macOS
./launchers/launch-tray.sh

# Windows
launchers\launch-tray.bat

# Cross-Platform
uv run python scripts/launch_tray.py
```

### Web Application Only

```bash
make serve            # Start development server
# Then open http://localhost:9001
```

## 📊 Project Status

**Current Status**: Production Ready ✅

- ✅ **Core Application**: Complete and functional
- ✅ **Desktop Tray App**: Cross-platform support
- ✅ **Documentation**: Comprehensive user and technical docs
- ✅ **Testing**: 100% test coverage
- ✅ **Code Quality**: Full linting compliance
- ✅ **CI/CD**: Automated builds and releases

## 🎯 Philosophy

> "They'll never notice it... until they need it, then it saves the day."

This portal is designed to be invisible during normal operations but indispensable during critical moments.

## 📞 Support

- **User Guide**: Complete usage instructions
- **Troubleshooting**: Common issues and solutions
- **Installation Guide**: Setup for all platforms
- **Technical Docs**: Architecture and implementation details

---

**Ready to get started?** Check out the [Installation Guide](installation.md) to begin!
