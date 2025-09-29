#!/usr/bin/env python3
"""
Add Graceful Degradation
Adds graceful degradation features to all HTML pages
"""

import glob
import re


def add_graceful_degradation(file_path):
    """Add graceful degradation to a single HTML file"""
    print(f"Processing {file_path}...")

    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    # Check if graceful degradation is already added
    if "Status Unknown (JS Disabled)" in content:
        print(f"  Already has graceful degradation: {file_path}")
        return

    # Add noscript fallback for status indicator
    # Find the status div and add noscript fallback after it
    status_pattern = r'(<div class="status online"[^>]*>Online</div>)'
    noscript_fallback = r'\1\n          <noscript>\n            <div class="status" style="background: var(--warning); color: white;">Status Unknown (JS Disabled)</div>\n          </noscript>'

    content = re.sub(status_pattern, noscript_fallback, content)

    # Add fallback for service worker registration
    # Add a comment explaining that service worker is optional
    if (
        "serviceWorker" in content
        and "<!-- Service Worker is optional -->" not in content
    ):
        service_worker_pattern = (
            r"(// Register service worker for offline functionality)"
        )
        service_worker_comment = (
            r"\1\n      // Note: Service worker is optional - site works without it"
        )
        content = re.sub(service_worker_pattern, service_worker_comment, content)

    # Write back to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  Added graceful degradation: {file_path}")


def main():
    """Main function to add graceful degradation to all pages"""
    print("Adding graceful degradation to all pages...")

    # Get all HTML files in pages directory
    html_files = glob.glob("pages/*.html")

    print(f"Found {len(html_files)} HTML files to process")

    for file_path in html_files:
        add_graceful_degradation(file_path)

    print("Graceful degradation addition complete!")
    print(f"Total files processed: {len(html_files)}")


if __name__ == "__main__":
    main()
