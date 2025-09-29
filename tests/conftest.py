"""
Pytest configuration and shared fixtures for the NIA Engineering Portal test suite.
"""

import os
import shutil
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest

# Set up environment for headless testing
if "DISPLAY" not in os.environ or not os.environ["DISPLAY"]:
    os.environ["DISPLAY"] = ":99"

from tray_app.config_manager import ConfigManager
from tray_app.server_controller import ServerController


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def test_config_manager(temp_dir: Path) -> ConfigManager:
    """Create a ConfigManager instance with test configuration."""
    # Create a test config file
    config_file = temp_dir / "test_config.json"

    # Create ConfigManager with test config
    config_manager = ConfigManager(str(config_file))

    # Set test configuration
    config_manager.set_port(9091)
    config_manager.set_default_page("index.html")

    return config_manager


@pytest.fixture
def test_server_controller(test_config_manager: ConfigManager) -> ServerController:
    """Create a ServerController instance for testing."""
    return ServerController(test_config_manager)


@pytest.fixture
def sample_html_files(temp_dir: Path) -> Generator[Path, None, None]:
    """Create sample HTML files for testing."""
    pages_dir = temp_dir / "pages"
    pages_dir.mkdir()

    # Create sample HTML files
    sample_files = [
        "index.html",
        "pages/plenary.html",
        "pages/committees.html",
        "pages/engineering.html",
        "pages/cr21.html",
        "pages/cr29.html",
        "pages/cr30.html",
        "pages/senate.html",
    ]

    for file_path in sample_files:
        full_path = temp_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(f"<html><body><h1>{file_path}</h1></body></html>")

    yield temp_dir


@pytest.fixture
def mock_webbrowser(monkeypatch):
    """Mock webbrowser module to prevent actual browser opening during tests."""
    import webbrowser

    opened_urls = []

    def mock_open(url):
        opened_urls.append(url)

    monkeypatch.setattr(webbrowser, "open", mock_open)
    return opened_urls
