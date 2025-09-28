#!/usr/bin/env python3
"""
Add Performance Monitoring Script
Adds performance monitoring to all HTML pages
"""

import os
import re
import glob

def add_performance_monitoring(file_path):
    """Add performance monitoring script to a single HTML file"""
    print(f"Processing {file_path}...")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if performance monitoring is already added
    if 'js/performance.js' in content:
        print(f"  Already has performance monitoring: {file_path}")
        return

    # Add performance monitoring script before closing body tag
    performance_script = '    \n    <!-- Performance Monitoring -->\n    <script src="js/performance.js"></script>\n'
    content = re.sub(r'(</body>)', performance_script + r'\1', content)

    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  Added performance monitoring: {file_path}")

def main():
    """Main function to add performance monitoring to all pages"""
    print("Adding performance monitoring to all pages...")

    # Get all HTML files in pages directory
    html_files = glob.glob('pages/*.html')

    print(f"Found {len(html_files)} HTML files to process")

    for file_path in html_files:
        add_performance_monitoring(file_path)

    print("Performance monitoring addition complete!")
    print(f"Total files processed: {len(html_files)}")

if __name__ == "__main__":
    main()
