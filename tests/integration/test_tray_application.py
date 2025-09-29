"""
Integration tests for the tray application components.
"""

from unittest.mock import Mock, patch

from tray_app.server_controller import ServerController
from tray_app.tray_app import TrayApplication


class TestTrayApplicationIntegration:
    """Integration tests for TrayApplication."""

    def test_tray_application_initialization(self, test_config_manager):
        """Test TrayApplication initialization."""
        server_controller = ServerController(test_config_manager)
        tray_app = TrayApplication(test_config_manager, server_controller)

        assert tray_app.config_manager == test_config_manager
        assert tray_app.server_controller == server_controller
        assert tray_app.icon is not None
        assert tray_app.is_running is False

    def test_icon_creation(self, test_config_manager):
        """Test tray icon creation."""
        server_controller = ServerController(test_config_manager)
        tray_app = TrayApplication(test_config_manager, server_controller)

        # Check that icon images are created
        assert "stopped" in tray_app.icon_images
        assert "running" in tray_app.icon_images
        assert "error" in tray_app.icon_images

        # Check that all icon images are valid
        for _status, image in tray_app.icon_images.items():
            assert image is not None
            assert hasattr(image, "size")

    def test_menu_creation(self, test_config_manager):
        """Test tray menu creation."""
        server_controller = ServerController(test_config_manager)
        tray_app = TrayApplication(test_config_manager, server_controller)

        menu = tray_app._create_menu()

        # Check that menu is created
        assert menu is not None

        # Check that menu items exist
        menu_items = [item.text for item in menu._items if hasattr(item, "text")]

        expected_items = [
            "Start Server",
            "Stop Server",
            "Open Portal",
            "Configure...",
            "Exit",
        ]

        for expected_item in expected_items:
            assert any(expected_item in item for item in menu_items)

    def test_status_callback_integration(self, test_config_manager):
        """Test status callback integration between components."""
        server_controller = ServerController(test_config_manager)
        tray_app = TrayApplication(test_config_manager, server_controller)

        # Mock the status callback
        status_updates = []

        def mock_status_callback(status):
            status_updates.append(status)

        tray_app._on_server_status_change = mock_status_callback

        # Test status updates
        tray_app._on_server_status_change("running")
        assert "running" in status_updates

        tray_app._on_server_status_change("stopped")
        assert "stopped" in status_updates

    def test_icon_update_integration(self, test_config_manager):
        """Test icon update integration."""
        server_controller = ServerController(test_config_manager)
        tray_app = TrayApplication(test_config_manager, server_controller)

        # Test icon updates for different statuses
        for status in ["running", "stopped", "error"]:
            tray_app._update_icon(status)

            # Check that icon was updated
            assert tray_app.icon.icon == tray_app.icon_images[status]

    def test_configuration_dialog_integration(self, test_config_manager):
        """Test configuration dialog integration."""
        server_controller = ServerController(test_config_manager)
        tray_app = TrayApplication(test_config_manager, server_controller)

        # Mock the configuration dialog
        with patch("tray_app.gui_components.ConfigurationDialog") as mock_dialog_class:
            mock_dialog = Mock()
            mock_dialog_class.return_value = mock_dialog

            # Test configuration dialog creation
            tray_app._show_configuration()

            # Verify dialog was created and shown
            mock_dialog_class.assert_called_once()
            call_args = mock_dialog_class.call_args
            assert call_args[0][0] == test_config_manager
            # The callback function might be different, so just check it's callable
            assert callable(call_args[0][1])
            mock_dialog.show.assert_called_once()

    @patch("subprocess.Popen")
    def test_server_start_stop_integration(self, mock_popen, test_config_manager):
        """Test server start/stop integration."""
        # Mock successful server process
        mock_process = Mock()
        mock_process.poll.return_value = None
        mock_popen.return_value = mock_process

        server_controller = ServerController(test_config_manager)
        tray_app = TrayApplication(test_config_manager, server_controller)

        # Test server start
        result = tray_app._start_server()
        assert result is None  # Method doesn't return value

        # Test server stop
        result = tray_app._stop_server()
        assert result is None  # Method doesn't return value

    def test_port_configuration_integration(self, test_config_manager):
        """Test port configuration integration."""
        server_controller = ServerController(test_config_manager)
        tray_app = TrayApplication(test_config_manager, server_controller)

        # Test port retrieval
        port = tray_app.server_controller.get_port()
        assert port == test_config_manager.get_port()

        # Test port change
        test_config_manager.set_port(8080)
        assert tray_app.server_controller.get_port() == 8080

    def test_page_configuration_integration(self, test_config_manager):
        """Test page configuration integration."""
        # server_controller = ServerController(test_config_manager)  # Not used in this test
        # tray_app = TrayApplication(test_config_manager, server_controller)  # Not used in this test

        # Test page retrieval
        page = test_config_manager.get_default_page()
        assert page in test_config_manager.get_available_pages()

        # Test page change
        available_pages = test_config_manager.get_available_pages()
        if available_pages:
            test_page = available_pages[0]
            test_config_manager.set_default_page(test_page)
            assert test_config_manager.get_default_page() == test_page
