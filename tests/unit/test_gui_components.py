"""
Unit tests for the GUI components.
"""

from pathlib import Path
from unittest.mock import Mock, patch

from tray_app.gui_components import ConfigurationDialog


class TestConfigurationDialog:
    """Test cases for ConfigurationDialog."""

    def test_initialization(self, test_config_manager):
        """Test ConfigurationDialog initialization."""
        dialog = ConfigurationDialog(test_config_manager)

        assert dialog.config_manager == test_config_manager
        assert dialog.on_save is None

    def test_initialization_with_callback(self, test_config_manager):
        """Test ConfigurationDialog initialization with callback."""
        callback = Mock()
        dialog = ConfigurationDialog(test_config_manager, callback)

        assert dialog.config_manager == test_config_manager
        assert dialog.on_save == callback

    def test_create_config_html(self, test_config_manager):
        """Test HTML configuration page creation."""
        dialog = ConfigurationDialog(test_config_manager)
        html = dialog._create_config_html(9092)

        # Check HTML structure
        assert "<!DOCTYPE html>" in html
        assert "<html" in html
        assert "<head>" in html
        assert "<body>" in html

        # Check form elements
        assert 'id="configForm"' in html
        assert 'id="port"' in html
        assert 'id="page"' in html

        # Check JavaScript
        assert "fetch(" in html
        assert "http://localhost:9092/save_config" in html

        # Check current values
        assert str(test_config_manager.get_port()) in html
        assert test_config_manager.get_default_page() in html

    def test_create_config_html_with_different_port(self, test_config_manager):
        """Test HTML creation with different port."""
        dialog = ConfigurationDialog(test_config_manager)
        html = dialog._create_config_html(8080)

        assert "http://localhost:8080/save_config" in html

    def test_create_config_html_includes_available_pages(self, test_config_manager):
        """Test that HTML includes all available pages."""
        dialog = ConfigurationDialog(test_config_manager)
        html = dialog._create_config_html(9092)

        available_pages = test_config_manager.get_available_pages()

        for page in available_pages:
            assert f'value="{page}"' in html or f">{page}</option>" in html

    @patch("webbrowser.open")
    @patch("threading.Thread")
    @patch("socketserver.TCPServer")
    @patch("http.server.SimpleHTTPRequestHandler")
    def test_show_method(
        self, mock_handler, mock_server, mock_thread, mock_open, test_config_manager
    ):
        """Test the show method."""
        dialog = ConfigurationDialog(test_config_manager)

        mock_httpd = Mock()
        mock_server.return_value = mock_httpd

        dialog.show()

        # Verify server was created and started
        mock_server.assert_called_once()
        mock_thread.assert_called()

        # Verify browser was opened
        mock_open.assert_called_once()

        # Verify HTML file was created
        config_file = Path(__file__).parent.parent.parent / "tray_app" / "config.html"
        assert config_file.exists()

        # Clean up
        if config_file.exists():
            config_file.unlink()

    def test_html_validation(self, test_config_manager):
        """Test HTML validation and structure."""
        dialog = ConfigurationDialog(test_config_manager)
        html = dialog._create_config_html(9092)

        # Check for proper form validation
        assert 'type="number"' in html
        assert 'min="1024"' in html
        assert 'max="65535"' in html
        assert "required" in html

        # Check for proper styling
        assert "style=" in html or "<style>" in html

        # Check for JavaScript functionality
        assert "addEventListener" in html
        assert "preventDefault" in html
        assert "fetch(" in html

    def test_html_cors_handling(self, test_config_manager):
        """Test that HTML includes proper CORS handling."""
        dialog = ConfigurationDialog(test_config_manager)
        html = dialog._create_config_html(9092)

        # Check for CORS headers in the fetch request
        assert "Content-Type" in html
        assert "application/json" in html

    def test_html_error_handling(self, test_config_manager):
        """Test that HTML includes proper error handling."""
        dialog = ConfigurationDialog(test_config_manager)
        html = dialog._create_config_html(9092)

        # Check for error handling in JavaScript
        assert "catch(" in html
        assert "showStatus" in html
        assert "error" in html.lower()

    def test_html_success_handling(self, test_config_manager):
        """Test that HTML includes proper success handling."""
        dialog = ConfigurationDialog(test_config_manager)
        html = dialog._create_config_html(9092)

        # Check for success handling in JavaScript
        assert "success" in html.lower()
        assert "window.close" in html
        assert "setTimeout" in html
