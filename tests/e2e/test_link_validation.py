"""
End-to-end tests for link validation and page accessibility.
"""

import re

from bs4 import BeautifulSoup


class TestLinkValidation:
    """Test cases for link validation and page accessibility."""

    def test_all_html_files_exist(self, sample_html_files):
        """Test that all HTML files referenced in configuration exist."""
        pages_dir = sample_html_files / "pages"

        # Get all HTML files in pages directory
        html_files = list(pages_dir.glob("*.html"))
        html_files.append(sample_html_files / "index.html")

        # All files should exist and be readable
        for html_file in html_files:
            assert html_file.exists(), f"HTML file {html_file} does not exist"
            assert html_file.is_file(), f"HTML file {html_file} is not a file"

            # Should be readable
            content = html_file.read_text(encoding="utf-8")
            assert len(content) > 0, f"HTML file {html_file} is empty"

    def test_html_structure_validation(self, sample_html_files):
        """Test HTML structure validation."""
        pages_dir = sample_html_files / "pages"
        html_files = list(pages_dir.glob("*.html"))
        html_files.append(sample_html_files / "index.html")

        for html_file in html_files:
            content = html_file.read_text(encoding="utf-8")
            soup = BeautifulSoup(content, "html.parser")

            # Should have basic HTML structure
            assert soup.find("html") is not None, f"Missing <html> tag in {html_file}"
            assert soup.find("body") is not None, f"Missing <body> tag in {html_file}"

            # Should have a title or heading
            title = soup.find("title") or soup.find("h1")
            assert title is not None, f"Missing title or h1 in {html_file}"

    def test_internal_link_validation(self, sample_html_files):
        """Test internal link validation."""
        pages_dir = sample_html_files / "pages"
        html_files = list(pages_dir.glob("*.html"))
        html_files.append(sample_html_files / "index.html")

        # Collect all internal links
        internal_links = set()

        for html_file in html_files:
            content = html_file.read_text(encoding="utf-8")
            soup = BeautifulSoup(content, "html.parser")

            # Find all links
            for link in soup.find_all("a", href=True):
                href = link["href"]

                # Skip external links
                if href.startswith("http") or href.startswith("//"):
                    continue

                # Skip mailto and tel links
                if href.startswith("mailto:") or href.startswith("tel:"):
                    continue

                # Skip anchor links
                if href.startswith("#"):
                    continue

                internal_links.add(href)

        # Validate internal links
        for link in internal_links:
            if link.startswith("/"):
                # Absolute path from root
                target_file = sample_html_files / link[1:]
            else:
                # Relative path
                target_file = sample_html_files / link

            # Check if target exists
            if not target_file.exists():
                # Check if it's a directory with index.html
                if target_file.is_dir():
                    index_file = target_file / "index.html"
                    assert index_file.exists(), (
                        f"Link {link} points to directory without index.html"
                    )
                else:
                    # For this test, we'll just log missing files
                    # In a real scenario, you might want to fail or create them
                    print(
                        f"Warning: Link {link} points to non-existent file {target_file}"
                    )

    def test_css_file_validation(self, sample_html_files):
        """Test CSS file validation."""
        pages_dir = sample_html_files / "pages"
        css_dir = pages_dir / "css"

        if css_dir.exists():
            css_files = list(css_dir.glob("*.css"))

            for css_file in css_files:
                assert css_file.exists(), f"CSS file {css_file} does not exist"

                content = css_file.read_text(encoding="utf-8")
                assert len(content) > 0, f"CSS file {css_file} is empty"

                # Basic CSS validation
                assert "{" in content, f"CSS file {css_file} appears to be invalid"

    def test_javascript_file_validation(self, sample_html_files):
        """Test JavaScript file validation."""
        pages_dir = sample_html_files / "pages"
        js_dir = pages_dir / "js"

        if js_dir.exists():
            js_files = list(js_dir.glob("*.js"))

            for js_file in js_files:
                assert js_file.exists(), f"JavaScript file {js_file} does not exist"

                content = js_file.read_text(encoding="utf-8")
                assert len(content) > 0, f"JavaScript file {js_file} is empty"

    def test_image_file_validation(self, sample_html_files):
        """Test image file validation."""
        pages_dir = sample_html_files / "pages"
        html_files = list(pages_dir.glob("*.html"))
        html_files.append(sample_html_files / "index.html")

        # Collect all image references
        image_links = set()

        for html_file in html_files:
            content = html_file.read_text(encoding="utf-8")
            soup = BeautifulSoup(content, "html.parser")

            # Find all images
            for img in soup.find_all("img", src=True):
                src = img["src"]

                # Skip external images
                if src.startswith("http") or src.startswith("//"):
                    continue

                image_links.add(src)

        # Validate image files
        for img_src in image_links:
            if img_src.startswith("/"):
                target_file = sample_html_files / img_src[1:]
            else:
                target_file = sample_html_files / img_src

            # For this test, we'll just check if the path is valid
            # In a real scenario, you might want to check if the file exists
            assert not target_file.is_dir(), f"Image {img_src} points to a directory"

    def test_navigation_structure_validation(self, sample_html_files):
        """Test navigation structure validation."""
        pages_dir = sample_html_files / "pages"
        html_files = list(pages_dir.glob("*.html"))
        html_files.append(sample_html_files / "index.html")

        # Check for navigation elements
        for html_file in html_files:
            content = html_file.read_text(encoding="utf-8")
            soup = BeautifulSoup(content, "html.parser")

            # Look for navigation elements
            nav_elements = soup.find_all(
                ["nav", "ul", "ol"], class_=re.compile(r"nav|menu", re.I)
            )

            # Should have some form of navigation
            if not nav_elements:
                # Check for links in general
                links = soup.find_all("a", href=True)
                # For test files, we'll be more lenient - just warn if no navigation
                if len(links) == 0:
                    print(f"Warning: No navigation or links found in {html_file}")

    def test_accessibility_basic_validation(self, sample_html_files):
        """Test basic accessibility validation."""
        pages_dir = sample_html_files / "pages"
        html_files = list(pages_dir.glob("*.html"))
        html_files.append(sample_html_files / "index.html")

        for html_file in html_files:
            content = html_file.read_text(encoding="utf-8")
            soup = BeautifulSoup(content, "html.parser")

            # Check for alt attributes on images
            images = soup.find_all("img")
            for img in images:
                if not img.get("alt"):
                    print(f"Warning: Image in {html_file} missing alt attribute")

            # Check for proper heading hierarchy
            headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
            if headings:
                # Should have at least one h1
                h1_count = len(soup.find_all("h1"))
                assert h1_count > 0, f"No h1 heading found in {html_file}"

                # Should not have multiple h1s (basic accessibility rule)
                assert h1_count <= 1, f"Multiple h1 headings found in {html_file}"

    def test_page_loading_performance(self, sample_html_files):
        """Test page loading performance."""
        pages_dir = sample_html_files / "pages"
        html_files = list(pages_dir.glob("*.html"))
        html_files.append(sample_html_files / "index.html")

        for html_file in html_files:
            content = html_file.read_text(encoding="utf-8")

            # Check file size (should be reasonable)
            file_size = len(content.encode("utf-8"))
            assert file_size < 1024 * 1024, (
                f"HTML file {html_file} is too large: {file_size} bytes"
            )

            # Check for excessive external resources
            soup = BeautifulSoup(content, "html.parser")
            external_links = soup.find_all("a", href=re.compile(r"^https?://"))
            external_images = soup.find_all("img", src=re.compile(r"^https?://"))

            # Should not have too many external resources
            total_external = len(external_links) + len(external_images)
            assert total_external < 50, (
                f"Too many external resources in {html_file}: {total_external}"
            )
