#!/usr/bin/env python3
"""
NIA Engineering Portal - Desktop Tray Application
Main entry point for the desktop tray application.
"""

import sys
import os
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tray_app.tray_app import TrayApplication
from tray_app.config_manager import ConfigManager
from tray_app.server_controller import ServerController

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nia_tray_app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main application entry point."""
    try:
        logger.info("Starting NIA Engineering Portal Tray Application")

        # Initialize configuration manager
        config_manager = ConfigManager()

        # Initialize server controller
        server_controller = ServerController(config_manager)

        # Initialize and run tray application
        tray_app = TrayApplication(config_manager, server_controller)
        tray_app.run()

    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
