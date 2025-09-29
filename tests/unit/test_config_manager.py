"""
Unit tests for the ConfigManager class.
"""

import json
import tempfile
from pathlib import Path

from tray_app.config_manager import ConfigManager


class TestConfigManager:
    """Test cases for ConfigManager."""

    def test_initialization_with_default_config(self):
        """Test ConfigManager initialization with default configuration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = Path(temp_dir) / "test_config.json"
            config_manager = ConfigManager(str(config_file))

            assert config_manager.get_port() == 9091
            assert config_manager.get_default_page() == "index.html"
            assert len(config_manager.get_available_pages()) > 0

    def test_port_validation(self):
        """Test port validation functionality."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = Path(temp_dir) / "test_config.json"
            config_manager = ConfigManager(str(config_file))

            # Valid ports
            assert config_manager.set_port(8080) is True
            assert config_manager.get_port() == 8080

            assert config_manager.set_port(3000) is True
            assert config_manager.get_port() == 3000

            # Invalid ports
            assert config_manager.set_port(80) is False  # Too low
            assert config_manager.set_port(70000) is False  # Too high
            assert config_manager.set_port(-1) is False  # Negative

            # Port should remain unchanged after invalid attempts
            assert config_manager.get_port() == 3000

    def test_page_validation(self):
        """Test page validation functionality."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = Path(temp_dir) / "test_config.json"
            config_manager = ConfigManager(str(config_file))

            available_pages = config_manager.get_available_pages()

            # Valid pages
            for page in available_pages:
                assert config_manager.set_default_page(page) is True
                assert config_manager.get_default_page() == page

            # Invalid page
            assert config_manager.set_default_page("nonexistent.html") is False
            # Should remain at last valid page
            assert config_manager.get_default_page() in available_pages

    def test_config_persistence(self):
        """Test configuration persistence to file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = Path(temp_dir) / "test_config.json"

            # Create and modify config
            config_manager = ConfigManager(str(config_file))
            config_manager.set_port(8080)
            config_manager.set_default_page("pages/plenary.html")
            config_manager.save_config()

            # Verify file was created
            assert config_file.exists()

            # Load config from file
            with open(config_file) as f:
                saved_config = json.load(f)

            assert saved_config["port"] == 8080
            assert saved_config["default_page"] == "pages/plenary.html"

    def test_config_loading_from_existing_file(self):
        """Test loading configuration from existing file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = Path(temp_dir) / "test_config.json"

            # Create config file manually
            test_config = {
                "port": 3000,
                "default_page": "pages/engineering.html",
                "available_pages": ["index.html", "pages/engineering.html"],
            }

            with open(config_file, "w") as f:
                json.dump(test_config, f)

            # Load config
            config_manager = ConfigManager(str(config_file))

            assert config_manager.get_port() == 3000
            assert config_manager.get_default_page() == "pages/engineering.html"

    def test_invalid_config_handling(self):
        """Test handling of invalid configuration files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = Path(temp_dir) / "test_config.json"

            # Create invalid JSON file
            with open(config_file, "w") as f:
                f.write("invalid json content")

            # Should fall back to default config
            config_manager = ConfigManager(str(config_file))
            assert config_manager.get_port() == 9091
            assert config_manager.get_default_page() == "index.html"

    def test_available_pages_completeness(self):
        """Test that all available pages are valid."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = Path(temp_dir) / "test_config.json"
            config_manager = ConfigManager(str(config_file))

            available_pages = config_manager.get_available_pages()

            # Should have multiple pages
            assert len(available_pages) > 5

            # Should include main pages
            assert "index.html" in available_pages
            assert "pages/plenary.html" in available_pages
            assert "pages/committees.html" in available_pages
            assert "pages/engineering.html" in available_pages

            # All pages should be strings
            for page in available_pages:
                assert isinstance(page, str)
                assert len(page) > 0
