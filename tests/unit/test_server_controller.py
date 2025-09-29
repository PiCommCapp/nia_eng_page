"""
Unit tests for the ServerController class.
"""

from unittest.mock import Mock, patch

from tray_app.server_controller import ServerController


class TestServerController:
    """Test cases for ServerController."""

    def test_initialization(self, test_config_manager):
        """Test ServerController initialization."""
        controller = ServerController(test_config_manager)

        assert controller.config_manager == test_config_manager
        assert controller.is_running is False
        assert controller.server_process is None
        assert controller.server_thread is None

    def test_port_availability_check(self, test_server_controller):
        """Test port availability checking."""
        # Test with a port that should be available
        available_port = test_server_controller.find_available_port(9999)
        assert 9999 <= available_port <= 65535

        # Test is_port_available method
        assert test_server_controller.is_port_available(available_port) is True

    def test_status_callback(self, test_server_controller):
        """Test status callback functionality."""
        callback_calls = []

        def test_callback(status):
            callback_calls.append(status)

        test_server_controller.set_status_callback(test_callback)
        test_server_controller._notify_status("running")

        assert "running" in callback_calls

    def test_get_status(self, test_server_controller):
        """Test status retrieval."""
        # Initially stopped
        assert test_server_controller.get_status() == "stopped"

        # Mock running state
        test_server_controller.is_running = True
        test_server_controller.server_process = Mock()
        test_server_controller.server_process.poll.return_value = None

        assert test_server_controller.get_status() == "running"

    def test_get_port(self, test_config_manager):
        """Test port retrieval from config manager."""
        controller = ServerController(test_config_manager)
        assert controller.get_port() == test_config_manager.get_port()

    @patch("subprocess.Popen")
    def test_start_server_success(self, mock_popen, test_server_controller):
        """Test successful server start."""
        # Mock successful server process
        mock_process = Mock()
        mock_process.poll.return_value = None
        mock_popen.return_value = mock_process

        result = test_server_controller.start_server()

        assert result is True
        assert test_server_controller.is_running is True
        assert test_server_controller.server_process == mock_process

    @patch("subprocess.Popen")
    def test_start_server_failure(self, mock_popen, test_server_controller):
        """Test server start failure."""
        # Mock failed server process
        mock_process = Mock()
        mock_process.poll.return_value = 1  # Process exited with error
        mock_popen.return_value = mock_process

        result = test_server_controller.start_server()

        assert result is False
        assert test_server_controller.is_running is False

    def test_stop_server_when_not_running(self, test_server_controller):
        """Test stopping server when not running."""
        result = test_server_controller.stop_server()
        assert result is True

    def test_stop_server_when_running(self, test_server_controller):
        """Test stopping server when running."""
        # Mock running server
        mock_process = Mock()
        mock_process.wait.return_value = 0
        test_server_controller.is_running = True
        test_server_controller.server_process = mock_process

        result = test_server_controller.stop_server()

        assert result is True
        assert test_server_controller.is_running is False
        mock_process.terminate.assert_called_once()

    @patch("webbrowser.open")
    def test_open_browser_when_running(self, mock_open, test_server_controller):
        """Test opening browser when server is running."""
        test_server_controller.is_running = True
        test_server_controller.open_browser()

        mock_open.assert_called_once()
        call_args = mock_open.call_args[0][0]
        assert "localhost" in call_args
        assert str(test_server_controller.get_port()) in call_args

    def test_open_browser_when_not_running(self, test_server_controller):
        """Test opening browser when server is not running."""
        with patch("webbrowser.open") as mock_open:
            test_server_controller.is_running = False
            test_server_controller.open_browser()

            mock_open.assert_not_called()

    def test_find_available_port(self, test_server_controller):
        """Test finding available port."""
        # Test with a high port number that should be available
        port = test_server_controller.find_available_port(65000)
        assert 65000 <= port <= 65535

        # Test that the found port is actually available
        assert test_server_controller.is_port_available(port) is True
