"""
Main tray application for the NIA Engineering Portal.
Provides system tray integration with icon, menu, and status indication.
"""

import logging
import os
from unittest.mock import MagicMock

try:
    import pystray
    from PIL import Image, ImageDraw

    PYSRAY_AVAILABLE = True
except (ImportError, OSError):
    # Handle headless environments or missing dependencies
    if "DISPLAY" not in os.environ or not os.environ["DISPLAY"]:
        # Mock pystray for headless testing
        pystray = MagicMock()
        pystray.Icon = MagicMock()
        pystray.Menu = MagicMock()
        pystray.MenuItem = MagicMock()
        pystray.Menu.SEPARATOR = "---"

        # Mock PIL for headless testing
        Image = MagicMock()
        ImageDraw = MagicMock()
        PYSRAY_AVAILABLE = False
    else:
        raise

logger = logging.getLogger(__name__)


class TrayApplication:
    """Main tray application class."""

    def __init__(self, config_manager, server_controller):
        """Initialize tray application.

        Args:
            config_manager: Configuration manager instance
            server_controller: Server controller instance
        """
        self.config_manager = config_manager
        self.server_controller = server_controller
        self.icon = None
        self.is_running = False

        # Set up server status callback
        self.server_controller.set_status_callback(self._on_server_status_change)

        # Create tray icon
        self._create_tray_icon()

    def _create_tray_icon(self) -> None:
        """Create the system tray icon."""
        if not PYSRAY_AVAILABLE:
            # In headless environments, create mock icons
            self.icon_images = {
                "stopped": MagicMock(),
                "running": MagicMock(),
                "error": MagicMock(),
            }
            return

        # Create icon images for different states
        self.icon_images = {
            "stopped": self._create_icon_image("red"),
            "running": self._create_icon_image("green"),
            "error": self._create_icon_image("gray"),
        }

        # Create menu
        menu = self._create_menu()

        # Create tray icon
        self.icon = pystray.Icon(
            "NIA Engineering Portal",
            self.icon_images["stopped"],
            "NIA Engineering Portal - Server stopped",
            menu,
        )

    def _create_icon_image(self, color: str) -> Image.Image:
        """Create icon image with specified color.

        Args:
            color: Color name ('red', 'green', 'gray')

        Returns:
            PIL Image object
        """
        if not PYSRAY_AVAILABLE:
            # Return mock image for headless environments
            return MagicMock()
        # Create a simple "www" icon
        size = 64
        image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Color mapping
        colors = {
            "red": (255, 0, 0, 255),
            "green": (0, 255, 0, 255),
            "gray": (128, 128, 128, 255),
        }

        color_rgba = colors.get(color, colors["gray"])

        # Draw a simple "www" representation
        # Draw three circles representing "www"
        circle_radius = 8
        spacing = 12
        start_x = (size - (2 * spacing + 3 * circle_radius * 2)) // 2
        start_y = size // 2

        for i in range(3):
            x = start_x + i * (spacing + circle_radius * 2)
            draw.ellipse(
                [
                    x,
                    start_y - circle_radius,
                    x + circle_radius * 2,
                    start_y + circle_radius,
                ],
                fill=color_rgba,
            )

        return image

    def _create_menu(self) -> pystray.Menu:
        """Create the tray context menu.

        Returns:
            pystray Menu object
        """
        # Get current status for the menu text
        status = self.server_controller.get_status()
        port = self.server_controller.get_port()

        if status == "running":
            status_text = f"🟢 Server running on port {port}"
        elif status == "stopped":
            status_text = "🔴 Server stopped"
        else:
            status_text = "⚠️ Server error"

        return pystray.Menu(
            pystray.MenuItem(status_text, None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Start Server", self._start_server, default=True),
            pystray.MenuItem("Stop Server", self._stop_server),
            pystray.MenuItem("Open Portal", self._open_portal),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Configure...", self._show_configuration),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", self._exit_application),
        )

    def _update_status_text(self) -> None:
        """Update the status text in the menu."""
        if self.icon:
            # Create a new menu with updated status text
            menu = self._create_menu()
            self.icon.menu = menu

    def _start_server(self, icon=None, item=None) -> None:
        """Start the server."""
        logger.info("Starting server from tray menu")
        if self.server_controller.start_server():
            self._update_icon("running")
            self._update_status_text()
        else:
            self._update_icon("error")
            self._update_status_text()

    def _stop_server(self, icon=None, item=None) -> None:
        """Stop the server."""
        logger.info("Stopping server from tray menu")
        if self.server_controller.stop_server():
            self._update_icon("stopped")
            self._update_status_text()
        else:
            self._update_icon("error")
            self._update_status_text()

    def _open_portal(self, icon=None, item=None) -> None:
        """Open the portal in browser."""
        logger.info("Opening portal in browser")
        self.server_controller.open_browser()

    def _show_configuration(self, icon=None, item=None) -> None:
        """Show configuration dialog."""
        logger.info("Showing configuration dialog")
        from tray_app.gui_components import ConfigurationDialog

        def on_config_save():
            """Called when configuration is saved."""
            self._update_status_text()

        dialog = ConfigurationDialog(self.config_manager, on_config_save)
        dialog.show()

    def _exit_application(self, icon=None, item=None) -> None:
        """Exit the application."""
        logger.info("Exiting application")
        self.is_running = False
        self.server_controller.stop_server()
        self.icon.stop()

    def _on_server_status_change(self, status: str) -> None:
        """Handle server status changes.

        Args:
            status: New server status
        """
        logger.info(f"Server status changed to: {status}")
        self._update_icon(status)
        self._update_status_text()

    def _update_icon(self, status: str) -> None:
        """Update the tray icon based on status.

        Args:
            status: Server status ('running', 'stopped', 'error')
        """
        if self.icon and status in self.icon_images:
            self.icon.icon = self.icon_images[status]

            # Update tooltip
            port = self.server_controller.get_port()
            if status == "running":
                tooltip = f"NIA Engineering Portal - Server running on port {port}"
            elif status == "stopped":
                tooltip = "NIA Engineering Portal - Server stopped"
            else:
                tooltip = "NIA Engineering Portal - Server error"

            self.icon.title = tooltip

    def run(self) -> None:
        """Run the tray application."""
        if not PYSRAY_AVAILABLE:
            logger.info("Running in headless mode - tray icon not available")
            self.is_running = True
            return

        if self.icon:
            self.is_running = True
            logger.info("Starting tray application")
            self.icon.run()
        else:
            logger.error("Failed to create tray icon")

    def stop(self) -> None:
        """Stop the tray application."""
        self.is_running = False
        if not PYSRAY_AVAILABLE:
            logger.info("Stopping headless mode")
            return

        if self.icon:
            self.icon.stop()
