# NIA Engineering Portal

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/nia-engineering-portal/nia-engineering-portal)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue.svg)](https://nia-engineering-portal.github.io/nia-engineering-portal/)

A lightning-fast, mission-critical engineering portal for broadcast/AV infrastructure access with desktop tray application support.

## 🚀 Quick Start

```bash
# Install dependencies
make install

# Launch in background (no terminal needed)
make tray-bg

# Create desktop shortcut (optional)
make tray-shortcut
```

**That's it!** Look for the NIA Engineering Portal icon in your system tray.

## 📖 Documentation

📚 **[Full Documentation](https://nia-engineering-portal.github.io/nia-engineering-portal/)** - Complete user guides, installation instructions, and technical documentation

### Quick Links

- **[Installation Guide](https://nia-engineering-portal.github.io/nia-engineering-portal/installation/)** - Step-by-step setup
- **[User Guide](https://nia-engineering-portal.github.io/nia-engineering-portal/user-guide/)** - Complete user manual
- **[Troubleshooting](https://nia-engineering-portal.github.io/nia-engineering-portal/troubleshooting/)** - Problem solving guide
- **[Technical Docs](https://nia-engineering-portal.github.io/nia-engineering-portal/technical/)** - Architecture and deployment

## ✨ Features

- **🖥️ Desktop Tray Application**: Cross-platform system tray integration (Windows, macOS, Linux)
- **⚙️ Web-based Configuration**: Easy management through web interface
- **⚡ Instant Access**: Static HTML interface loads immediately
- **🧭 Intuitive Navigation**: Clean categorization of all systems
- **📱 Local Deployment**: Works offline, no external dependencies
- **🔄 Background Operation**: Runs without keeping terminal open
- **🎯 Zero Training**: Engineers can use it immediately

## 🎯 System Categories

- **KVM Switches**: AIM Main/Reserve access
- **Network Infrastructure**: Firewalls, Dante audio, control systems
- **Control Rooms**: CAR2, B23 committee rooms
- **Gallery Screens**: PDU management interfaces
- **Support Systems**: Busby admin, documentation

## 🚀 Installation

### Prerequisites

- Python 3.12 or higher
- Git
- [UV Package Manager](https://astral.sh/uv/) (installed automatically)

### Install & Run

```bash
# Clone the repository
git clone https://github.com/nia-engineering-portal/nia-engineering-portal.git
cd nia-engineering-portal

# Install dependencies
make install

# Launch application
make tray-bg
```

### Alternative Launch Methods

```bash
# Manual launchers
./launchers/launch-tray.sh        # Unix/Linux/macOS
launchers\launch-tray.bat         # Windows
uv run python scripts/launch_tray.py  # Cross-platform

# Web application only
make serve                        # Start development server
```

## 🛠️ Technical Stack

- **Backend**: Python 3.12+ with HTTP server
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Desktop**: PyInstaller, pystray for cross-platform tray application
- **Configuration**: JSON-based configuration management
- **Testing**: pytest with comprehensive test coverage
- **Build**: UV package manager, cross-platform makefile
- **CI/CD**: GitHub Actions for automated builds and releases

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

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [Full Documentation](https://nia-engineering-portal.github.io/nia-engineering-portal/)
- **Issues**: [GitHub Issues](https://github.com/nia-engineering-portal/nia-engineering-portal/issues)
- **Discussions**: [GitHub Discussions](https://github.com/nia-engineering-portal/nia-engineering-portal/discussions)

---

**Ready to get started?** Check out the [Installation Guide](https://nia-engineering-portal.github.io/nia-engineering-portal/installation/)!
