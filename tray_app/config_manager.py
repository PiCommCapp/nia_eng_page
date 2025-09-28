"""
Configuration management for the NIA Engineering Portal tray application.
Handles loading, saving, and validation of configuration settings.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ConfigManager:
    """Manages application configuration."""

    def __init__(self, config_file: str = "config.json"):
        """Initialize configuration manager.

        Args:
            config_file: Name of the configuration file
        """
        self.config_file = Path(__file__).parent / config_file
        self.default_config = {
            "port": 9091,
            "default_page": "index.html",
            "available_pages": [
                "index.html",
                "pages/plenary.html",
                "pages/committees/index.html",
                "pages/engineering/index.html"
            ]
        }
        # Initialize config as None first
        self.config = None
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default.

        Returns:
            Configuration dictionary
        """
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                logger.info(f"Configuration loaded from {self.config_file}")
                return self._validate_config(config)
            else:
                logger.info("Configuration file not found, creating default")
                return self._create_default_config()
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return self._create_default_config()

    def save_config(self) -> bool:
        """Save current configuration to file.

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"Configuration saved to {self.config_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return False

    def _validate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate configuration and fix any issues.

        Args:
            config: Configuration dictionary to validate

        Returns:
            Validated configuration dictionary
        """
        validated = self.default_config.copy()

        # Validate port
        if "port" in config and isinstance(config["port"], int):
            if 1024 <= config["port"] <= 65535:
                validated["port"] = config["port"]
            else:
                logger.warning(f"Invalid port {config['port']}, using default {self.default_config['port']}")

        # Validate default page
        if "default_page" in config and isinstance(config["default_page"], str):
            if config["default_page"] in self.default_config["available_pages"]:
                validated["default_page"] = config["default_page"]
            else:
                logger.warning(f"Invalid default page {config['default_page']}, using default {self.default_config['default_page']}")

        # Validate available pages (keep default if invalid)
        if "available_pages" in config and isinstance(config["available_pages"], list):
            if all(isinstance(page, str) for page in config["available_pages"]):
                validated["available_pages"] = config["available_pages"]

        return validated

    def _create_default_config(self) -> Dict[str, Any]:
        """Create and save default configuration.

        Returns:
            Default configuration dictionary
        """
        config = self.default_config.copy()
        # Save config directly without using self.config
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            logger.info(f"Default configuration saved to {self.config_file}")
        except Exception as e:
            logger.error(f"Error saving default configuration: {e}")
        return config

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value.

        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config[key] = value

    def get_port(self) -> int:
        """Get configured port number.

        Returns:
            Port number
        """
        return self.get("port", self.default_config["port"])

    def set_port(self, port: int) -> bool:
        """Set port number with validation.

        Args:
            port: Port number to set

        Returns:
            True if valid and set, False otherwise
        """
        if isinstance(port, int) and 1024 <= port <= 65535:
            self.set("port", port)
            return True
        return False

    def get_default_page(self) -> str:
        """Get default page.

        Returns:
            Default page path
        """
        return self.get("default_page", self.default_config["default_page"])

    def set_default_page(self, page: str) -> bool:
        """Set default page with validation.

        Args:
            page: Page path to set

        Returns:
            True if valid and set, False otherwise
        """
        available_pages = self.get("available_pages", self.default_config["available_pages"])
        if page in available_pages:
            self.set("default_page", page)
            return True
        return False

    def get_available_pages(self) -> list:
        """Get list of available pages.

        Returns:
            List of available page paths
        """
        return self.get("available_pages", self.default_config["available_pages"])
