# NIA Engineering Portal - Installation Guide

## 📋 Prerequisites

### System Requirements

- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.12 or higher
- **Memory**: 512MB RAM minimum
- **Disk Space**: 100MB for application and dependencies
- **Network**: Local network access (no internet required for operation)

### Required Software

- **UV Package Manager**: Modern Python package manager
- **Git**: For cloning the repository
- **Web Browser**: Any modern browser (Chrome, Firefox, Safari, Edge)

## 🚀 Installation Methods

### Method 1: Automated Installation (Recommended)

1. **Clone Repository**:

   ```bash
   git clone <repository-url>
   cd nia_eng_page
   ```

2. **Run Installation**:

   ```bash
   make install
   ```

3. **Verify Installation**:

   ```bash
   make status
   ```

### Method 2: Manual Installation

1. **Install UV Package Manager**:

   **Windows (PowerShell)**:

   ```powershell
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

   **macOS/Linux**:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone Repository**:

   ```bash
   git clone <repository-url>
   cd nia_eng_page
   ```

3. **Create Virtual Environment**:

   ```bash
   uv venv
   ```

4. **Install Dependencies**:

   ```bash
   uv sync
   ```

5. **Verify Installation**:
   ```bash
   uv run python --version
   uv run python -c "import tray_app; print('Installation successful')"
   ```

## 🔧 Platform-Specific Instructions

### Windows Installation

1. **Open PowerShell as Administrator**
2. **Install UV**:
   ```powershell
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
3. **Restart PowerShell**
4. **Clone and Install**:
   ```powershell
   git clone <repository-url>
   cd nia_eng_page
   make install
   ```

### macOS Installation

1. **Install Homebrew** (if not already installed):

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install UV**:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Add UV to PATH** (add to ~/.zshrc or ~/.bash_profile):

   ```bash
   echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

4. **Clone and Install**:
   ```bash
   git clone <repository-url>
   cd nia_eng_page
   make install
   ```

### Linux Installation

1. **Install System Dependencies**:

   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip git curl

   # CentOS/RHEL
   sudo yum install python3 python3-pip git curl
   ```

2. **Install UV**:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Add UV to PATH** (add to ~/.bashrc):

   ```bash
   echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

4. **Clone and Install**:
   ```bash
   git clone <repository-url>
   cd nia_eng_page
   make install
   ```

## ✅ Verification

### Check Installation

Run the following commands to verify your installation:

```bash
# Check system status
make status

# Check Python version
uv run python --version

# Check application components
make test-tray

# Check available commands
make help
```

### Expected Output

- **System Status**: Should show all components as working
- **Python Version**: Should be 3.12 or higher
- **Test Tray**: Should show all components working
- **Help**: Should display all available commands

## 🚀 First Launch

### Launch the Application

1. **Background Launch** (Recommended):

   ```bash
   make tray-bg
   ```

2. **Foreground Launch** (for debugging):

   ```bash
   make tray
   ```

3. **Create Desktop Shortcut** (Optional):
   ```bash
   make tray-shortcut
   ```

### Verify Launch

1. **Check Tray Icon**: Look for NIA Engineering Portal icon in system tray
2. **Open Portal**: Click the tray icon to open the web portal
3. **Test Navigation**: Navigate through the portal to ensure it works
4. **Check Configuration**: Right-click tray icon and select "Configure"

## 🔧 Configuration

### Initial Configuration

1. **Open Configuration**:

   - Right-click the tray icon
   - Select "Configure"

2. **Adjust Settings**:

   - **Port**: Default is 9001 (change if needed)
   - **Pages**: Select which pages to include
   - **Auto-start**: Enable to start with system

3. **Save Configuration**:
   - Click "Save" to apply changes
   - Restart the application if needed

### Configuration File

The configuration is stored in `tray_app/config.json`:

```json
{
  "port": 9001,
  "pages": ["committees", "engineering", "network"],
  "auto_start": false,
  "log_level": "INFO"
}
```

## 🐛 Troubleshooting Installation

### Common Issues

#### UV Not Found

- **Windows**: Restart PowerShell after installation
- **macOS/Linux**: Add UV to PATH in shell profile
- **Verify**: Run `uv --version` to check installation

#### Python Version Issues

- **Check Version**: `python3 --version` should show 3.12+
- **Install Python**: Install Python 3.12 or higher
- **Use UV**: UV will manage Python versions automatically

#### Permission Issues

- **Windows**: Run PowerShell as Administrator
- **macOS/Linux**: Check file permissions and ownership
- **Virtual Environment**: Ensure proper permissions on .venv directory

#### Port Already in Use

- **Check Port**: `netstat -an | grep 9001` (Unix) or `netstat -an | findstr 9001` (Windows)
- **Kill Process**: Stop the process using the port
- **Change Port**: Modify configuration to use different port

### Getting Help

1. **Check Logs**: Look at `nia_tray_app.log` for error messages
2. **Check Status**: Run `make status` to verify system state
3. **Check Dependencies**: Run `make install` to reinstall dependencies
4. **Check Documentation**: Review troubleshooting guides

## 📦 Uninstallation

### Remove Application

1. **Stop Application**:

   - Right-click tray icon and select "Quit"
   - Or run `make kill` to stop server

2. **Remove Files**:

   ```bash
   # Remove application directory
   rm -rf /path/to/nia_eng_page

   # Remove configuration (optional)
   rm -rf ~/.config/nia-engineering-portal
   ```

3. **Remove Dependencies** (Optional):
   ```bash
   # Remove UV (if not used for other projects)
   # Windows: Remove from Programs and Features
   # macOS: Remove from Applications
   # Linux: Remove from package manager
   ```

## 🔄 Updates

### Updating the Application

1. **Stop Application**:

   ```bash
   make kill
   ```

2. **Update Code**:

   ```bash
   git pull origin main
   ```

3. **Update Dependencies**:

   ```bash
   make update
   ```

4. **Restart Application**:
   ```bash
   make tray-bg
   ```

### Checking for Updates

```bash
# Check for code updates
git fetch
git status

# Check for dependency updates
uv sync --upgrade
```

---

## 📞 Support

### Self-Service

1. **Check This Guide**: Review all installation steps
2. **Check Logs**: Look at `nia_tray_app.log` for error details
3. **Check Status**: Run `make status` to verify system state
4. **Check Dependencies**: Run `make install` to reinstall

### Getting Additional Help

- **Documentation**: Check `docs/` folder for technical documentation
- **User Guide**: Review `docs/user-guide.md` for usage instructions
- **Troubleshooting**: Check `docs/troubleshooting.md` for common issues
- **Logs**: Provide log file contents when reporting issues

---

_Last Updated: December 2024_
_Version: 1.0.0_
_Status: Production Ready_
