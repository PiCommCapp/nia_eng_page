#!/usr/bin/env python3
"""
Simple HTTP server for NIA Engineering Portal static site.
Serves static files and handles root redirect to pages/ directory.
"""

import http.server
import socketserver
import os
import sys
from urllib.parse import urlparse


class RedirectHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler that redirects root to pages/ directory."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)

    def do_GET(self):
        """Handle GET requests with root redirect logic."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # Handle root redirect to pages/
        if path == '/' or path == '':
            self.send_response(302)
            self.send_header('Location', '/pages/')
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'Redirecting to <a href="/pages/">NIA Engineering Portal</a>...')
            return

        # Handle pages/ directory requests
        if path.startswith('/pages/'):
            # Remove /pages/ prefix and serve from pages directory
            relative_path = path[7:]  # Remove '/pages/' prefix
            if not relative_path:
                relative_path = 'index.html'

            # Check if file exists in pages directory
            pages_path = os.path.join('pages', relative_path)
            if os.path.exists(pages_path) and os.path.isfile(pages_path):
                self.path = f'/pages/{relative_path}'
            else:
                # If file doesn't exist, try index.html
                if os.path.exists(os.path.join('pages', 'index.html')):
                    self.path = '/pages/index.html'
                else:
                    self.send_error(404, "File not found")
                    return

        # Call parent method to handle the request
        super().do_GET()

    def end_headers(self):
        """Add CORS headers for development."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()


def main():
    """Start the HTTP server."""
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 9001))

    # Change to the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)

    # Create server
    with socketserver.TCPServer(("", port), RedirectHandler) as httpd:
        print(f"🚀 NIA Engineering Portal Server")
        print(f"📁 Serving from: {project_root}")
        print(f"🌐 Server running at: http://localhost:{port}")
        print(f"📄 Portal available at: http://localhost:{port}/pages/")
        print(f"⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
            sys.exit(0)


if __name__ == "__main__":
    main()
