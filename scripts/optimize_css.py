#!/usr/bin/env python3
"""
CSS Optimization Script
Replaces inline CSS with external CSS file for better performance
"""

import glob
import re


def extract_css_from_html(html_content):
    """Extract CSS content from HTML file"""
    # Find the style tag and extract its content
    style_match = re.search(r"<style>(.*?)</style>", html_content, re.DOTALL)
    if style_match:
        return style_match.group(1).strip()
    return None


def replace_css_with_link(html_content):
    """Replace inline CSS with link to external CSS file"""
    # Remove the entire style section
    html_content = re.sub(r"<style>.*?</style>", "", html_content, flags=re.DOTALL)

    # Add link to external CSS before closing head tag
    css_link = '    <link rel="stylesheet" href="css/common.css" />\n'
    html_content = re.sub(r"(</head>)", css_link + r"\1", html_content)

    return html_content


def optimize_html_file(file_path):
    """Optimize a single HTML file"""
    print(f"Processing {file_path}...")

    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    # Check if file already has external CSS link
    if "css/common.css" in content:
        print(f"  Already optimized: {file_path}")
        return

    # Replace inline CSS with external link
    optimized_content = replace_css_with_link(content)

    # Write back to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(optimized_content)

    print(f"  Optimized: {file_path}")


def main():
    """Main optimization function"""
    print("Starting CSS optimization...")

    # Get all HTML files in pages directory
    html_files = glob.glob("pages/*.html")

    print(f"Found {len(html_files)} HTML files to optimize")

    for file_path in html_files:
        optimize_html_file(file_path)

    print("CSS optimization complete!")
    print(f"Total files processed: {len(html_files)}")


if __name__ == "__main__":
    main()
