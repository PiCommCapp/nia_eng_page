# NIA Engineering Portal - Makefile

# Default port for the development server
PORT ?= 9001

.PHONY: help serve serve-port install update clean status kill tray build-tray test-tray lint lint-fix lint-python lint-js format format-python format-js check

# Default target
help:
	@echo "NIA Engineering Portal - Available Commands:"
	@echo ""
	@echo "  make serve      - Start the development server (port $(PORT))"
	@echo "  make serve-port - Start server with custom port (PORT=3000 make serve-port)"
	@echo "  make kill       - Kill any running server instances"
	@echo "  make install    - Install UV and Python dependencies"
	@echo "  make update     - Update dependencies using UV"
	@echo "  make status     - Check project status and dependencies"
	@echo "  make clean      - Clean up temporary files"
	@echo ""
	@echo "Code Quality Commands:"
	@echo "  make lint       - Run all linters (Python + JavaScript)"
	@echo "  make lint-fix   - Run linters and auto-fix issues"
	@echo "  make lint-python- Run Python linting with Ruff"
	@echo "  make lint-js    - Run JavaScript/HTML linting with ESLint"
	@echo "  make format     - Format all code (Python + JavaScript)"
	@echo "  make format-python- Format Python code with Ruff"
	@echo "  make format-js  - Format JavaScript/HTML with Prettier"
	@echo "  make check      - Run comprehensive code quality check"
	@echo ""
	@echo "Tray Application Commands:"
	@echo "  make tray       - Run the tray application (requires display)"
	@echo "  make tray-bg    - Run the tray application in background (no terminal needed)"
	@echo "  make tray-shortcut - Create desktop shortcut for the application"
	@echo "  make test-tray  - Test tray application components"
	@echo "  make build-tray - Build executable for current platform"
	@echo ""
	@echo "Testing Commands:"
	@echo "  make test       - Run all tests (unit, integration, e2e, performance, accessibility)"
	@echo "  make test-unit  - Run unit tests only"
	@echo "  make test-integration - Run integration tests only"
	@echo "  make test-e2e   - Run end-to-end tests only"
	@echo "  make test-performance - Run performance tests only"
	@echo "  make test-accessibility - Run accessibility tests only"
	@echo "  make test-coverage - Run all tests with coverage report"
	@echo ""
	@echo "Version Management Commands:"
	@echo "  make version    - Get current version"
	@echo "  make version-bump TYPE=<patch|minor|major> - Bump version"
	@echo "  make version-set VERSION=<x.y.z> - Set specific version"
	@echo "  make version-info - Show detailed version information"
	@echo ""
	@echo "Release Commands:"
	@echo "  make release-build - Build release packages (with tests)"
	@echo "  make release-build-fast - Build release packages (skip tests)"
	@echo "  make release-clean - Clean release artifacts"
	@echo ""
	@echo "Launcher Commands:"
	@echo "  make tray-bg       - Launch tray app in background (no terminal needed)"
	@echo "  make tray-shortcut - Create desktop shortcut for easy launching"
	@echo "  ./launchers/launch-tray.sh - Unix/Linux/macOS launcher script"
	@echo "  launchers\\launch-tray.bat - Windows launcher script"
	@echo ""

# Start the development server
serve:
	@echo "🚀 Starting NIA Engineering Portal server..."
	@echo "📍 Server will be available at: http://localhost:$(PORT)"
	@echo "🛑 Press Ctrl+C to stop the server"
	@echo ""
	PORT=$(PORT) uv run python scripts/serve.py

# Start server with custom port
serve-port:
	@echo "🚀 Starting NIA Engineering Portal server on port $(PORT)..."
	@echo "📍 Server will be available at: http://localhost:$(PORT)"
	@echo "🛑 Press Ctrl+C to stop the server"
	@echo ""
	PORT=$(PORT) uv run python scripts/serve.py

# Kill any running server instances
kill:
	@echo "🛑 Stopping NIA Engineering Portal server instances..."
	@echo "  • Killing processes on port $(PORT)..."
	@$(MAKE) kill-unix || $(MAKE) kill-windows

# Unix/Linux/macOS kill command
kill-unix:
	@if lsof -ti:$(PORT) > /dev/null 2>&1; then \
		echo "  • Found process on port $(PORT)"; \
		lsof -ti:$(PORT) | xargs kill -9 2>/dev/null || true; \
		echo "✅ Server process on port $(PORT) stopped"; \
	else \
		echo "  • No process found on port $(PORT)"; \
	fi
	@echo "✅ Kill command completed!"

# Windows kill command
kill-windows:
	@for /f "tokens=5" %%a in ('netstat -ano ^| findstr :$(PORT)') do ( \
		echo "  • Found process %%a on port $(PORT)"; \
		taskkill /PID %%a /F >nul 2>&1 || echo "  • Process %%a already stopped"; \
	)
	@echo "✅ Kill command completed!"

# Install Python dependencies
install:
	@echo "📦 Checking UV installation..."
	@$(MAKE) check-uv-unix || $(MAKE) check-uv-windows
	@echo "🔧 Creating virtual environment and installing dependencies..."
	uv venv
	uv sync
	@echo "✅ Installation complete!"

# Check UV on Unix/Linux/macOS
check-uv-unix:
	@which uv > /dev/null || (echo "❌ UV not found. Please install UV first:" && echo "   curl -LsSf https://astral.sh/uv/install.sh | sh" && exit 1)
	@echo "✅ UV found at $$(which uv)"

# Check UV on Windows
check-uv-windows:
	@where uv >nul 2>&1 || (echo "❌ UV not found. Please install UV first:" && echo "   powershell -c \"irm https://astral.sh/uv/install.ps1 | iex\"" && exit 1)
	@echo "✅ UV found at $$(where uv)"

# Update dependencies
update:
	@echo "🔄 Updating dependencies using UV..."
	uv sync --upgrade
	@echo "✅ Dependencies updated successfully"

# Check project status
status:
	@echo "📊 NIA Engineering Portal - Project Status"
	@echo ""
	@echo "🔧 Environment:"
	@$(MAKE) status-env-unix || $(MAKE) status-env-windows
	@echo ""
	@echo "📁 Project Structure:"
	@$(MAKE) status-structure-unix || $(MAKE) status-structure-windows
	@echo ""
	@echo "📦 Dependencies:"
	@$(MAKE) status-deps-unix || $(MAKE) status-deps-windows
	@echo ""

# Environment status for Unix/Linux/macOS
status-env-unix:
	@echo "  • Python: $$(python3 --version 2>/dev/null || echo 'Not found')"
	@echo "  • UV: $$(uv --version 2>/dev/null || echo 'Not found')"
	@echo "  • Virtual Environment: $$(if [ -d .venv ]; then echo '✅ Created'; else echo '❌ Not created'; fi)"

# Environment status for Windows
status-env-windows:
	@echo "  • Python: $$(python --version 2>nul || echo 'Not found')"
	@echo "  • UV: $$(uv --version 2>nul || echo 'Not found')"
	@echo "  • Virtual Environment: $$(if exist .venv (echo '✅ Created') else (echo '❌ Not created'))"

# Project structure status for Unix/Linux/macOS
status-structure-unix:
	@echo "  • Pages Directory: $$(if [ -d pages ]; then echo '✅ Exists'; else echo '❌ Missing'; fi)"
	@echo "  • Scripts Directory: $$(if [ -d scripts ]; then echo '✅ Exists'; else echo '❌ Missing'; fi)"
	@echo "  • Documentation: $$(if [ -d docs ]; then echo '✅ Exists'; else echo '❌ Missing'; fi)"

# Project structure status for Windows
status-structure-windows:
	@echo "  • Pages Directory: $$(if exist pages (echo '✅ Exists') else (echo '❌ Missing'))"
	@echo "  • Scripts Directory: $$(if exist scripts (echo '✅ Exists') else (echo '❌ Missing'))"
	@echo "  • Documentation: $$(if exist docs (echo '✅ Exists') else (echo '❌ Missing'))"

# Dependencies status for Unix/Linux/macOS
status-deps-unix:
	@if [ -f pyproject.toml ]; then \
		echo "  • Project Config: ✅ pyproject.toml found"; \
		if [ -d .venv ]; then \
			echo "  • Dependencies: $$(uv pip list --format=freeze | wc -l | tr -d ' ') packages installed"; \
		else \
			echo "  • Dependencies: ❌ Virtual environment not created"; \
		fi; \
	else \
		echo "  • Project Config: ❌ pyproject.toml not found"; \
	fi

# Dependencies status for Windows
status-deps-windows:
	@if exist pyproject.toml ( \
		echo "  • Project Config: ✅ pyproject.toml found" && \
		if exist .venv ( \
			for /f %%i in ('uv pip list --format=freeze ^| find /c /v ""') do echo "  • Dependencies: %%i packages installed" \
		) else ( \
			echo "  • Dependencies: ❌ Virtual environment not created" \
		) \
	) else ( \
		echo "  • Project Config: ❌ pyproject.toml not found" \
	)

# Clean up temporary files
clean:
	@echo "🧹 Cleaning up temporary files..."
	@echo "  • Removing Python cache files..."
	@$(MAKE) clean-unix || $(MAKE) clean-windows
	@echo "✅ Cleanup complete"
	@echo ""

# Clean for Unix/Linux/macOS
clean-unix:
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type d -name "__pycache__" -delete 2>/dev/null || true
	@echo "  • Removing build artifacts..."
	@rm -rf build/ dist/ *.spec

# Clean for Windows
clean-windows:
	@for /r . %%i in (*.pyc) do del "%%i" 2>nul || true
	@for /d /r . %%i in (__pycache__) do rmdir /s /q "%%i" 2>nul || true
	@echo "  • Removing build artifacts..."
	@if exist build rmdir /s /q build
	@if exist dist rmdir /s /q dist
	@del *.spec 2>nul || true

# Tray Application Commands

# Run the tray application (requires display)
tray:
	@echo "🖥️  Starting NIA Engineering Portal Tray Application..."
	@echo "⚠️  Note: This requires a display (X11/Wayland on Linux)"
	@echo ""
	uv run python tray_app/main.py

# Run the tray application in background (no terminal needed)
tray-bg:
	@echo "🖥️  Starting NIA Engineering Portal Tray Application in background..."
	@echo "✅ You can close this terminal window"
	@echo ""
	@$(MAKE) tray-bg-unix || $(MAKE) tray-bg-windows

# Background launch for Unix/Linux/macOS
tray-bg-unix:
	@nohup uv run python tray_app/main.py > /dev/null 2>&1 &
	@echo "✅ Tray application started in background"
	@echo "🖥️  Look for the NIA Engineering Portal icon in your system tray"
	@echo "🛑 To stop the application, right-click the tray icon and select 'Quit'"

# Background launch for Windows
tray-bg-windows:
	@start /B uv run python tray_app/main.py
	@echo "✅ Tray application started in background"
	@echo "🖥️  Look for the NIA Engineering Portal icon in your system tray"
	@echo "🛑 To stop the application, right-click the tray icon and select 'Quit'"

# Create desktop shortcut for the application
tray-shortcut:
	@echo "🖥️  Creating desktop shortcut for NIA Engineering Portal..."
	@uv run python scripts/create_desktop_shortcut.py
	@echo "✅ Desktop shortcut created successfully!"

# Test tray application components
test-tray:
	@echo "🧪 Testing tray application components..."
	@echo "  • Testing configuration manager..."
	@uv run python -c "from tray_app.config_manager import ConfigManager; cm = ConfigManager(); print('✓ Config manager working')"
	@echo "  • Testing server controller..."
	@uv run python -c "from tray_app.server_controller import ServerController; from tray_app.config_manager import ConfigManager; cm = ConfigManager(); sc = ServerController(cm); print('✓ Server controller working')"
	@echo "  • Testing GUI components..."
	@uv run python -c "from tray_app.gui_components import ConfigurationDialog; from tray_app.config_manager import ConfigManager; cm = ConfigManager(); print('✓ GUI components working')"
	@echo "✅ All tray application components working"
	@echo ""

# Build executable for current platform
build-tray:
	@echo "🔨 Building tray application executable..."
	@echo "  • Platform: $$(uname -s)"
	@echo "  • Using PyInstaller with UV..."
	@uv run python scripts/build_tray.py
	@echo "✅ Build complete"
	@echo "  • Executable location: dist/$$(uname -s | tr '[:upper:]' '[:lower:]')/"
	@echo ""

# Testing Commands

# Run all tests
test:
	@echo "🧪 Running all tests..."
	@echo "  • Unit tests..."
	@$(MAKE) test-unit
	@echo "  • Integration tests..."
	@$(MAKE) test-integration
	@echo "  • End-to-end tests..."
	@$(MAKE) test-e2e
	@echo "  • Performance tests..."
	@$(MAKE) test-performance
	@echo "  • Accessibility tests..."
	@$(MAKE) test-accessibility
	@echo "✅ All tests complete"
	@echo ""

# Run unit tests
test-unit:
	@echo "🔬 Running unit tests..."
	@if [ -d .venv ]; then \
		uv run python tests/run_tests.py unit; \
	else \
		echo "❌ Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@echo "✅ Unit tests complete"
	@echo ""

# Run integration tests
test-integration:
	@echo "🔗 Running integration tests..."
	@if [ -d .venv ]; then \
		uv run python tests/run_tests.py integration; \
	else \
		echo "❌ Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@echo "✅ Integration tests complete"
	@echo ""

# Run end-to-end tests
test-e2e:
	@echo "🌐 Running end-to-end tests..."
	@if [ -d .venv ]; then \
		uv run python tests/run_tests.py e2e; \
	else \
		echo "❌ Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@echo "✅ End-to-end tests complete"
	@echo ""

# Run performance tests
test-performance:
	@echo "⚡ Running performance tests..."
	@if [ -d .venv ]; then \
		uv run python tests/run_tests.py performance; \
	else \
		echo "❌ Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@echo "✅ Performance tests complete"
	@echo ""

# Run accessibility tests
test-accessibility:
	@echo "♿ Running accessibility tests..."
	@if [ -d .venv ]; then \
		uv run python tests/run_tests.py accessibility; \
	else \
		echo "❌ Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@echo "✅ Accessibility tests complete"
	@echo ""

# Run tests with coverage
test-coverage:
	@echo "📊 Running tests with coverage..."
	@if [ -d .venv ]; then \
		uv run python tests/run_tests.py all --verbose; \
	else \
		echo "❌ Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@echo "✅ Coverage report generated"
	@echo ""

# Version Management Commands

# Get current version
version:
	@echo "📋 Current version:"
	@uv run python scripts/version.py get

# Bump version (patch, minor, major)
version-bump:
	@if [ -z "$(TYPE)" ]; then \
		echo "❌ Please specify version type: make version-bump TYPE=patch|minor|major"; \
		exit 1; \
	fi
	@echo "🔄 Bumping $(TYPE) version..."
	@uv run python scripts/version.py bump $(TYPE)

# Set specific version
version-set:
	@if [ -z "$(VERSION)" ]; then \
		echo "❌ Please specify version: make version-set VERSION=1.2.3"; \
		exit 1; \
	fi
	@echo "🔧 Setting version to $(VERSION)..."
	@uv run python scripts/version.py set $(VERSION)

# Show version info
version-info:
	@echo "📋 Version information:"
	@uv run python scripts/version.py info

# Release Commands

# Build release packages
release-build:
	@echo "🚀 Building release packages..."
	@if [ -d .venv ]; then \
		uv run python scripts/build_release.py; \
	else \
		echo "❌ Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@echo "✅ Release build complete"
	@echo ""

# Build release packages (skip tests)
release-build-fast:
	@echo "🚀 Building release packages (skipping tests)..."
	@if [ -d .venv ]; then \
		uv run python scripts/build_release.py --skip-tests; \
	else \
		echo "❌ Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@echo "✅ Release build complete"
	@echo ""

# Clean release artifacts
release-clean:
	@echo "🧹 Cleaning release artifacts..."
	@rm -rf dist/ build/
	@echo "✅ Release artifacts cleaned"
	@echo ""

# Code Quality Commands

# Run all linters
lint:
	@echo "🔍 Running all linters..."
	@echo "  • Python linting with Ruff..."
	@$(MAKE) lint-python
	@echo "  • JavaScript/HTML linting with ESLint..."
	@$(MAKE) lint-js
	@echo "✅ All linting complete"
	@echo ""

# Run linters and auto-fix issues
lint-fix:
	@echo "🔧 Running linters with auto-fix..."
	@echo "  • Auto-fixing Python issues..."
	@$(MAKE) format-python
	@echo "  • Auto-fixing JavaScript/HTML issues..."
	@$(MAKE) format-js
	@echo "✅ Auto-fix complete"
	@echo ""

# Run Python linting with Ruff
lint-python:
	@echo "🐍 Running Python linting with Ruff..."
	@if [ -d .venv ]; then \
		uv run ruff check .; \
	else \
		echo "❌ Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@echo "✅ Python linting complete"
	@echo ""

# Run JavaScript/HTML linting with ESLint
lint-js:
	@echo "📜 Running JavaScript/HTML linting with ESLint..."
	@if command -v npx > /dev/null 2>&1; then \
		npx eslint pages/js/ scripts/ --ext .js,.html || echo "⚠️  ESLint found issues (see output above)"; \
	else \
		echo "⚠️  npx not found. Install Node.js and npm to use ESLint."; \
	fi
	@echo "✅ JavaScript/HTML linting complete"
	@echo ""

# Format all code
format:
	@echo "✨ Formatting all code..."
	@echo "  • Formatting Python code..."
	@$(MAKE) format-python
	@echo "  • Formatting JavaScript/HTML code..."
	@$(MAKE) format-js
	@echo "✅ All formatting complete"
	@echo ""

# Format Python code with Ruff
format-python:
	@echo "🐍 Formatting Python code with Ruff..."
	@if [ -d .venv ]; then \
		uv run ruff format . && uv run ruff check --fix .; \
	else \
		echo "❌ Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@echo "✅ Python formatting complete"
	@echo ""

# Format JavaScript/HTML code with Prettier
format-js:
	@echo "📜 Formatting JavaScript/HTML code with Prettier..."
	@if command -v npx > /dev/null 2>&1; then \
		npx prettier --write "pages/**/*.{js,html,css}" "scripts/**/*.js" "*.html" "*.md" || echo "⚠️  Prettier found issues (see output above)"; \
	else \
		echo "⚠️  npx not found. Install Node.js and npm to use Prettier."; \
	fi
	@echo "✅ JavaScript/HTML formatting complete"
	@echo ""

# Run comprehensive code quality check
check:
	@echo "🔍 Running comprehensive code quality check..."
	@echo "  • Checking Python code quality..."
	@$(MAKE) lint-python
	@echo "  • Checking JavaScript/HTML code quality..."
	@$(MAKE) lint-js
	@echo "  • Checking code formatting..."
	@echo "    - Python formatting check..."
	@if [ -d .venv ]; then \
		uv run ruff format --check . && echo "✅ Python formatting is correct"; \
	else \
		echo "❌ Virtual environment not found. Run 'make install' first."; \
	fi
	@echo "    - JavaScript/HTML formatting check..."
	@if command -v npx > /dev/null 2>&1; then \
		npx prettier --check "pages/**/*.{js,html,css}" "scripts/**/*.js" "*.html" "*.md" && echo "✅ JavaScript/HTML formatting is correct"; \
	else \
		echo "⚠️  npx not found. Install Node.js and npm to use Prettier."; \
	fi
	@echo "✅ Comprehensive code quality check complete"
	@echo ""
