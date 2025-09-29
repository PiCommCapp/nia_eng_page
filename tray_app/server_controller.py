"""
Server controller for the NIA Engineering Portal tray application.
Manages the web server process, including start/stop and port conflict handling.
"""

import logging
import os
import socket
import subprocess
import threading
import time
import webbrowser
from collections.abc import Callable
from pathlib import Path

logger = logging.getLogger(__name__)


class ServerController:
    """Manages the web server process."""

    def __init__(self, config_manager):
        """Initialize server controller.

        Args:
            config_manager: Configuration manager instance
        """
        self.config_manager = config_manager
        self.server_process: subprocess.Popen | None = None
        self.server_thread: threading.Thread | None = None
        self.is_running = False
        self.status_callback: Callable | None = None

        # Get the project root directory
        self.project_root = Path(__file__).parent.parent
        self.serve_script = self.project_root / "scripts" / "serve.py"

    def set_status_callback(self, callback: Callable) -> None:
        """Set callback function for status updates.

        Args:
            callback: Function to call with status updates
        """
        self.status_callback = callback

    def _notify_status(self, status: str) -> None:
        """Notify status callback if set.

        Args:
            status: Status message
        """
        if self.status_callback:
            self.status_callback(status)

    def is_port_available(self, port: int) -> bool:
        """Check if a port is available.

        Args:
            port: Port number to check

        Returns:
            True if port is available, False otherwise
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("localhost", port))
                return True
        except OSError:
            return False

    def find_available_port(self, start_port: int) -> int:
        """Find an available port starting from the given port.

        Args:
            start_port: Port to start checking from

        Returns:
            Available port number
        """
        port = start_port
        while port <= 65535:
            if self.is_port_available(port):
                return port
            port += 1

        # If no port found, return the original port (will show error)
        return start_port

    def start_server(self) -> bool:
        """Start the web server.

        Returns:
            True if server started successfully, False otherwise
        """
        if self.is_running:
            logger.warning("Server is already running")
            return True

        port = self.config_manager.get_port()

        # Check if port is available
        if not self.is_port_available(port):
            logger.warning(f"Port {port} is not available, finding alternative")
            available_port = self.find_available_port(port)
            if available_port != port:
                logger.info(f"Using port {available_port} instead of {port}")
                port = available_port
            else:
                logger.error("No available ports found")
                self._notify_status("error")
                return False

        try:
            # Set environment variables
            env = os.environ.copy()
            env["PORT"] = str(port)

            # Start the server process
            self.server_process = subprocess.Popen(
                ["uv", "run", "python", str(self.serve_script)],
                cwd=str(self.project_root),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # Start monitoring thread
            self.server_thread = threading.Thread(target=self._monitor_server)
            self.server_thread.daemon = True
            self.server_thread.start()

            # Wait a moment for server to start
            time.sleep(1)

            if self.server_process.poll() is None:
                self.is_running = True
                logger.info(f"Server started on port {port}")
                self._notify_status("running")
                return True
            else:
                logger.error("Server failed to start")
                self._notify_status("error")
                return False

        except Exception as e:
            logger.error(f"Error starting server: {e}")
            self._notify_status("error")
            return False

    def stop_server(self) -> bool:
        """Stop the web server.

        Returns:
            True if server stopped successfully, False otherwise
        """
        if not self.is_running or self.server_process is None:
            logger.warning("Server is not running")
            return True

        try:
            self.server_process.terminate()

            # Wait for graceful shutdown
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                logger.warning("Server did not stop gracefully, forcing kill")
                self.server_process.kill()
                self.server_process.wait()

            self.is_running = False
            logger.info("Server stopped")
            self._notify_status("stopped")
            return True

        except Exception as e:
            logger.error(f"Error stopping server: {e}")
            self._notify_status("error")
            return False

    def _monitor_server(self) -> None:
        """Monitor server process in background thread."""
        try:
            while self.server_process and self.server_process.poll() is None:
                time.sleep(1)

            # Server process ended
            if self.is_running:
                logger.warning("Server process ended unexpectedly")
                self.is_running = False
                self._notify_status("stopped")

        except Exception as e:
            logger.error(f"Error monitoring server: {e}")
            self.is_running = False
            self._notify_status("error")

    def open_browser(self) -> None:
        """Open the portal in the default browser."""
        if not self.is_running:
            logger.warning("Server is not running, cannot open browser")
            return

        port = self.config_manager.get_port()
        default_page = self.config_manager.get_default_page()

        # Construct URL
        if default_page == "index.html":
            url = f"http://localhost:{port}/"
        else:
            url = f"http://localhost:{port}/{default_page}"

        try:
            webbrowser.open(url)
            logger.info(f"Opened browser to {url}")
        except Exception as e:
            logger.error(f"Error opening browser: {e}")

    def get_status(self) -> str:
        """Get current server status.

        Returns:
            Status string: 'running', 'stopped', or 'error'
        """
        if (
            self.is_running
            and self.server_process
            and self.server_process.poll() is None
        ):
            return "running"
        elif not self.is_running:
            return "stopped"
        else:
            return "error"

    def get_port(self) -> int:
        """Get current server port.

        Returns:
            Port number
        """
        return self.config_manager.get_port()
