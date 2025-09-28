"""
GUI components for the NIA Engineering Portal tray application.
Provides the configuration dialog and other user interface elements.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable
import logging

logger = logging.getLogger(__name__)

class ConfigurationDialog:
    """Configuration dialog for the tray application."""

    def __init__(self, config_manager, on_save: Optional[Callable] = None):
        """Initialize configuration dialog.

        Args:
            config_manager: Configuration manager instance
            on_save: Callback function called when configuration is saved
        """
        self.config_manager = config_manager
        self.on_save = on_save
        self.dialog = None
        self.port_var = None
        self.page_var = None

    def show(self) -> None:
        """Show the configuration dialog."""
        if self.dialog and self.dialog.winfo_exists():
            self.dialog.lift()
            return

        self.dialog = tk.Toplevel()
        self.dialog.title("NIA Engineering Portal Configuration")
        self.dialog.geometry("400x200")
        self.dialog.resizable(False, False)

        # Center the dialog
        self.dialog.transient()
        self.dialog.grab_set()

        self._create_widgets()
        self._load_current_config()

        # Center on screen
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (200 // 2)
        self.dialog.geometry(f"400x200+{x}+{y}")

    def _create_widgets(self) -> None:
        """Create dialog widgets."""
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Port configuration
        port_frame = ttk.LabelFrame(main_frame, text="Server Port", padding="10")
        port_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(port_frame, text="Port:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))

        self.port_var = tk.StringVar()
        port_entry = ttk.Entry(port_frame, textvariable=self.port_var, width=10)
        port_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))

        ttk.Button(port_frame, text="Test Port", command=self._test_port).grid(row=0, column=2, sticky=tk.W)

        # Page selection
        page_frame = ttk.LabelFrame(main_frame, text="Default Page", padding="10")
        page_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))

        ttk.Label(page_frame, text="Page:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))

        self.page_var = tk.StringVar()
        page_combo = ttk.Combobox(page_frame, textvariable=self.page_var, width=30, state="readonly")
        page_combo.grid(row=0, column=1, sticky=(tk.W, tk.E))

        # Load available pages
        available_pages = self.config_manager.get_available_pages()
        page_combo['values'] = available_pages

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))

        ttk.Button(button_frame, text="Save", command=self._save_config).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="Cancel", command=self._close_dialog).grid(row=0, column=1)

        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        page_frame.columnconfigure(1, weight=1)

    def _load_current_config(self) -> None:
        """Load current configuration into dialog."""
        self.port_var.set(str(self.config_manager.get_port()))
        self.page_var.set(self.config_manager.get_default_page())

    def _test_port(self) -> None:
        """Test if the configured port is available."""
        try:
            port = int(self.port_var.get())
            if 1024 <= port <= 65535:
                # Import here to avoid circular imports
                from tray_app.server_controller import ServerController
                controller = ServerController(self.config_manager)
                if controller.is_port_available(port):
                    messagebox.showinfo("Port Test", f"Port {port} is available")
                else:
                    messagebox.showwarning("Port Test", f"Port {port} is not available")
            else:
                messagebox.showerror("Port Test", "Port must be between 1024 and 65535")
        except ValueError:
            messagebox.showerror("Port Test", "Please enter a valid port number")

    def _save_config(self) -> None:
        """Save configuration."""
        try:
            # Validate port
            port = int(self.port_var.get())
            if not (1024 <= port <= 65535):
                messagebox.showerror("Invalid Port", "Port must be between 1024 and 65535")
                return

            # Validate page
            page = self.page_var.get()
            available_pages = self.config_manager.get_available_pages()
            if page not in available_pages:
                messagebox.showerror("Invalid Page", "Please select a valid page")
                return

            # Save configuration
            self.config_manager.set_port(port)
            self.config_manager.set_default_page(page)

            if self.config_manager.save_config():
                messagebox.showinfo("Configuration Saved", "Configuration saved successfully")
                if self.on_save:
                    self.on_save()
                self._close_dialog()
            else:
                messagebox.showerror("Save Error", "Failed to save configuration")

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid port number")

    def _close_dialog(self) -> None:
        """Close the dialog."""
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None
