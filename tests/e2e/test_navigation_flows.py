"""
End-to-end tests for navigation flows and page functionality.
"""

import json
import tempfile
from pathlib import Path

from tray_app.config_manager import ConfigManager
from tray_app.gui_components import ConfigurationDialog
from tray_app.server_controller import ServerController


class TestNavigationFlows:
    """End-to-end tests for navigation flows."""

    def test_configuration_dialog_flow(self, test_config_manager):
        """Test complete configuration dialog flow."""
        dialog = ConfigurationDialog(test_config_manager)

        # Test HTML generation
        html = dialog._create_config_html(9092)
        assert "http://localhost:9092/save_config" in html

        # Test that all available pages are included
        available_pages = test_config_manager.get_available_pages()
        for page in available_pages:
            assert page in html

    def test_server_start_stop_flow(self, test_config_manager):
        """Test complete server start/stop flow."""
        server_controller = ServerController(test_config_manager)

        # Test initial state
        assert server_controller.get_status() == "stopped"
        assert not server_controller.is_running

        # Test port availability
        port = server_controller.get_port()
        assert (
            server_controller.is_port_available(port)
            or server_controller.find_available_port(port) != port
        )

    def test_configuration_persistence_flow(self, test_config_manager):
        """Test configuration persistence flow."""
        # Set new configuration
        test_config_manager.set_port(8080)
        test_config_manager.set_default_page("pages/plenary.html")
        test_config_manager.save_config()

        # Verify configuration was saved
        assert test_config_manager.get_port() == 8080
        assert test_config_manager.get_default_page() == "pages/plenary.html"

        # Test loading configuration
        config_file = test_config_manager.config_file
        assert config_file.exists()

        with open(config_file) as f:
            saved_config = json.load(f)

        assert saved_config["port"] == 8080
        assert saved_config["default_page"] == "pages/plenary.html"

    def test_page_validation_flow(self, test_config_manager):
        """Test page validation flow."""
        available_pages = test_config_manager.get_available_pages()

        # Test valid pages
        for page in available_pages[:5]:  # Test first 5 pages
            assert test_config_manager.set_default_page(page) is True
            assert test_config_manager.get_default_page() == page

        # Test invalid page
        assert test_config_manager.set_default_page("nonexistent.html") is False
        # Should remain at last valid page
        assert test_config_manager.get_default_page() in available_pages

    def test_port_validation_flow(self, test_config_manager):
        """Test port validation flow."""
        # Test valid ports
        valid_ports = [3000, 8080, 9091, 30000]
        for port in valid_ports:
            assert test_config_manager.set_port(port) is True
            assert test_config_manager.get_port() == port

        # Test invalid ports
        invalid_ports = [80, 443, 1023, 65536, -1]
        for port in invalid_ports:
            assert test_config_manager.set_port(port) is False
            # Port should remain unchanged
            assert test_config_manager.get_port() == 30000  # Last valid port

    def test_configuration_dialog_http_server_flow(self, test_config_manager):
        """Test configuration dialog HTTP server flow."""
        dialog = ConfigurationDialog(test_config_manager)

        # Test HTML generation instead of full show method
        html = dialog._create_config_html(9092)

        # Verify HTML contains server endpoint
        assert "http://localhost:9092/save_config" in html

        # Verify HTML contains form elements
        assert 'id="configForm"' in html
        assert 'id="port"' in html
        assert 'id="page"' in html

    def test_error_handling_flow(self, test_config_manager):
        """Test error handling flow."""
        # Test with invalid configuration file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("invalid json")
            invalid_config_file = f.name

        try:
            # Should handle invalid JSON gracefully
            config_manager = ConfigManager(invalid_config_file)
            assert config_manager.get_port() == 9091  # Default port
            assert config_manager.get_default_page() == "index.html"  # Default page
        finally:
            Path(invalid_config_file).unlink()

    def test_available_pages_completeness_flow(self, test_config_manager):
        """Test that all available pages are complete and valid."""
        available_pages = test_config_manager.get_available_pages()

        # Should have multiple pages
        assert len(available_pages) > 10

        # Should include main categories
        main_categories = [
            "index.html",
            "pages/plenary.html",
            "pages/committees.html",
            "pages/engineering.html",
        ]

        for category in main_categories:
            assert category in available_pages

        # All pages should be strings and non-empty
        for page in available_pages:
            assert isinstance(page, str)
            assert len(page) > 0
            assert page.endswith(".html")

    def test_configuration_validation_flow(self, test_config_manager):
        """Test configuration validation flow."""
        # Test valid configuration
        valid_config = {
            "port": 8080,
            "default_page": "pages/plenary.html",
            "available_pages": ["index.html", "pages/plenary.html"],
        }

        # Test configuration validation
        validated_config = test_config_manager._validate_config(valid_config)
        assert validated_config["port"] == 8080
        assert validated_config["default_page"] == "pages/plenary.html"

        # Test invalid configuration
        invalid_config = {
            "port": 80,  # Too low
            "default_page": "nonexistent.html",
            "available_pages": "not_a_list",
        }

        validated_config = test_config_manager._validate_config(invalid_config)
        # Should fall back to defaults
        assert validated_config["port"] == 9091
        assert validated_config["default_page"] == "index.html"
