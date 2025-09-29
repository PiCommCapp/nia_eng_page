"""
GUI components for the NIA Engineering Portal tray application.
Provides the configuration dialog and other user interface elements.
"""

import logging
import webbrowser
from collections.abc import Callable
from pathlib import Path

logger = logging.getLogger(__name__)


class ConfigurationDialog:
    """Configuration dialog for the tray application."""

    def __init__(self, config_manager, on_save: Callable | None = None):
        """Initialize configuration dialog.

        Args:
            config_manager: Configuration manager instance
            on_save: Callback function called when configuration is saved
        """
        self.config_manager = config_manager
        self.on_save = on_save

    def show(self) -> None:
        """Show the configuration dialog by opening a web page."""
        logger.info("Opening configuration web page")

        # Start a simple HTTP server to handle configuration updates
        import http.server
        import json
        import socketserver
        import threading
        import time

        # Capture variables for use in the handler
        config_manager = self.config_manager
        on_save = self.on_save

        class ConfigHandler(http.server.SimpleHTTPRequestHandler):
            def end_headers(self):
                # Add CORS headers
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type")
                super().end_headers()

            def do_OPTIONS(self):
                # Handle preflight requests
                self.send_response(200)
                self.end_headers()

            def do_POST(self):
                if self.path == "/save_config":
                    content_length = int(self.headers["Content-Length"])
                    post_data = self.rfile.read(content_length)
                    try:
                        config_data = json.loads(post_data.decode("utf-8"))

                        # Update configuration
                        config_manager.set_port(config_data["port"])
                        config_manager.set_default_page(config_data["default_page"])
                        config_manager.save_config()

                        # Send success response
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        response = {
                            "status": "success",
                            "message": "Configuration saved successfully",
                        }
                        self.wfile.write(json.dumps(response).encode("utf-8"))

                        # Call the callback if provided
                        if on_save:
                            on_save()

                    except Exception as e:
                        # Send error response
                        self.send_response(400)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        response = {"status": "error", "message": str(e)}
                        self.wfile.write(json.dumps(response).encode("utf-8"))
                else:
                    self.send_response(404)
                    self.end_headers()

        # Find an available port for the config server
        config_port = 9092
        while True:
            try:
                httpd = socketserver.TCPServer(("", config_port), ConfigHandler)
                break
            except OSError:
                config_port += 1

        # Start the server in a separate thread
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        # Give the server a moment to start
        time.sleep(0.5)

        # Create the configuration HTML with the server URL
        config_html = self._create_config_html(config_port)

        # Write to a temporary file
        config_file = Path(__file__).parent / "config.html"
        with open(config_file, "w") as f:
            f.write(config_html)

        # Open in browser
        webbrowser.open(f"file://{config_file.absolute()}")

        # Show instructions
        print("\n" + "=" * 60)
        print("🔧 NIA Engineering Portal Configuration")
        print("=" * 60)
        print("A configuration page has opened in your browser.")
        print("Make your changes and click 'Save Configuration' to apply them.")
        print("The configuration will be saved automatically.")
        print("=" * 60)

        # Clean up after a delay (no user interaction required)
        def cleanup_after_delay():
            time.sleep(30)  # Give user time to configure
            if config_file.exists():
                config_file.unlink()
            # Shutdown the server
            try:
                httpd.shutdown()
            except Exception:
                # Ignore shutdown errors during cleanup
                pass

        cleanup_thread = threading.Thread(target=cleanup_after_delay)
        cleanup_thread.daemon = True
        cleanup_thread.start()

    def _create_config_html(self, config_port: int = 9092) -> str:
        """Create HTML configuration page."""
        current_port = self.config_manager.get_port()
        current_page = self.config_manager.get_default_page()
        available_pages = self.config_manager.get_available_pages()

        page_options = ""
        for page in available_pages:
            selected = "selected" if page == current_page else ""
            page_options += f'<option value="{page}" {selected}>{page}</option>'

        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NIA Engineering Portal - Configuration</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            margin-bottom: 30px;
            text-align: center;
        }}
        .form-group {{
            margin-bottom: 20px;
        }}
        label {{
            display: block;
            margin-bottom: 5px;
            font-weight: 500;
            color: #555;
        }}
        input, select {{
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }}
        button {{
            background-color: #007bff;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin-right: 10px;
        }}
        button:hover {{
            background-color: #0056b3;
        }}
        .secondary {{
            background-color: #6c757d;
        }}
        .secondary:hover {{
            background-color: #545b62;
        }}
        .status {{
            margin-top: 20px;
            padding: 10px;
            border-radius: 4px;
            display: none;
        }}
        .success {{
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }}
        .error {{
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔧 NIA Engineering Portal Configuration</h1>

        <form id="configForm">
            <div class="form-group">
                <label for="port">Server Port:</label>
                <input type="number" id="port" name="port" value="{current_port}" min="1024" max="65535" required>
                <small>Port must be between 1024 and 65535</small>
            </div>

            <div class="form-group">
                <label for="page">Default Page:</label>
                <select id="page" name="page" required>
                    {page_options}
                </select>
            </div>

            <div class="form-group">
                <button type="button" onclick="testPort()">Test Port</button>
                <button type="submit">Save Configuration</button>
                <button type="button" onclick="window.close()" class="secondary">Close</button>
            </div>

            <div id="status" class="status"></div>
        </form>
    </div>

    <script>
        function showStatus(message, type) {{
            const status = document.getElementById('status');
            status.textContent = message;
            status.className = 'status ' + type;
            status.style.display = 'block';
            setTimeout(() => {{
                status.style.display = 'none';
            }}, 3000);
        }}

        function testPort() {{
            const port = document.getElementById('port').value;
            if (port < 1024 || port > 65535) {{
                showStatus('Port must be between 1024 and 65535', 'error');
                return;
            }}
            showStatus('Port test not available in web interface. Please test manually.', 'error');
        }}

        document.getElementById('configForm').addEventListener('submit', function(e) {{
            e.preventDefault();

            const port = parseInt(document.getElementById('port').value);
            const page = document.getElementById('page').value;

            if (port < 1024 || port > 65535) {{
                showStatus('Port must be between 1024 and 65535', 'error');
                return;
            }}

            // Save configuration via HTTP POST to the tray app
            const configData = {{
                port: port,
                default_page: page
            }};

            fetch('http://localhost:{config_port}/save_config', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                }},
                body: JSON.stringify(configData)
            }})
            .then(response => response.json())
            .then(data => {{
                if (data.status === 'success') {{
                    showStatus('Configuration saved successfully! The tray application has been updated.', 'success');
                    // Close the window after a short delay
                    setTimeout(() => {{
                        window.close();
                    }}, 2000);
                }} else {{
                    showStatus('Error saving configuration: ' + data.message, 'error');
                }}
            }})
            .catch(error => {{
                showStatus('Error saving configuration: ' + error.message, 'error');
            }});
        }});
    </script>
</body>
</html>
"""
