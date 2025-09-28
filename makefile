# NIA Engineering Portal - Makefile

# Default port for the development server
PORT ?= 9001

.PHONY: help serve serve-port install update clean status kill tray build-tray test-tray

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
	@echo "Tray Application Commands:"
	@echo "  make tray       - Run the tray application (requires display)"
	@echo "  make test-tray  - Test tray application components"
	@echo "  make build-tray - Build executable for current platform"
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
	@if lsof -ti:$(PORT) > /dev/null 2>&1; then \
		echo "  • Found process on port $(PORT)"; \
		lsof -ti:$(PORT) | xargs kill -9 2>/dev/null || true; \
		echo "✅ Server process on port $(PORT) stopped"; \
	else \
		echo "  • No process found on port $(PORT)"; \
	fi
	@echo "✅ Kill command completed!"

# Install Python dependencies
install:
	@echo "📦 Checking UV installation..."
	@which uv > /dev/null || (echo "❌ UV not found. Please install UV first:" && echo "   curl -LsSf https://astral.sh/uv/install.sh | sh" && exit 1)
	@echo "✅ UV found at $$(which uv)"
	@echo "🔧 Creating virtual environment and installing dependencies..."
	uv venv
	uv sync
	@echo "✅ Installation complete!"

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
	@echo "  • Python: $$(python3 --version 2>/dev/null || echo 'Not found')"
	@echo "  • UV: $$(uv --version 2>/dev/null || echo 'Not found')"
	@echo "  • Virtual Environment: $$(if [ -d .venv ]; then echo '✅ Created'; else echo '❌ Not created'; fi)"
	@echo ""
	@echo "📁 Project Structure:"
	@echo "  • Pages Directory: $$(if [ -d pages ]; then echo '✅ Exists'; else echo '❌ Missing'; fi)"
	@echo "  • Scripts Directory: $$(if [ -d scripts ]; then echo '✅ Exists'; else echo '❌ Missing'; fi)"
	@echo "  • Documentation: $$(if [ -d docs ]; then echo '✅ Exists'; else echo '❌ Missing'; fi)"
	@echo ""
	@echo "📦 Dependencies:"
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
	@echo ""

# Clean up temporary files
clean:
	@echo "🧹 Cleaning up temporary files..."
	@echo "  • Removing Python cache files..."
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type d -name "__pycache__" -delete 2>/dev/null || true
	@echo "  • Removing system files..."
	@echo "  • Removing build artifacts..."
	@rm -rf build/ dist/ *.spec
	@echo "✅ Cleanup complete"
	@echo ""

# Tray Application Commands

# Run the tray application (requires display)
tray:
	@echo "🖥️  Starting NIA Engineering Portal Tray Application..."
	@echo "⚠️  Note: This requires a display (X11/Wayland on Linux)"
	@echo ""
	uv run python tray_app/main.py

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
