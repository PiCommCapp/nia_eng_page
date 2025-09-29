#!/usr/bin/env python3
"""
Version management script for NIA Engineering Portal.
Handles version bumping, validation, and synchronization across files.
"""

import re
import sys
from pathlib import Path


class VersionManager:
    """Manages version numbers across the project."""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path(__file__).parent.parent
        self.pyproject_file = self.project_root / "pyproject.toml"
        self.version_file = self.project_root / "VERSION"

    def get_current_version(self) -> str:
        """Get the current version from pyproject.toml."""
        if not self.pyproject_file.exists():
            raise FileNotFoundError("pyproject.toml not found")

        content = self.pyproject_file.read_text()
        match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
        if not match:
            raise ValueError("Version not found in pyproject.toml")
        return match.group(1)

    def parse_version(self, version: str) -> tuple[int, int, int]:
        """Parse version string into major, minor, patch components."""
        match = re.match(r"^(\d+)\.(\d+)\.(\d+)$", version)
        if not match:
            raise ValueError(f"Invalid version format: {version}")
        return tuple(map(int, match.groups()))

    def format_version(self, major: int, minor: int, patch: int) -> str:
        """Format version components into version string."""
        return f"{major}.{minor}.{patch}"

    def bump_version(self, version_type: str) -> str:
        """Bump version by type: major, minor, or patch."""
        current = self.get_current_version()
        major, minor, patch = self.parse_version(current)

        if version_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif version_type == "minor":
            minor += 1
            patch = 0
        elif version_type == "patch":
            patch += 1
        else:
            raise ValueError(
                f"Invalid version type: {version_type}. Use: major, minor, patch"
            )

        return self.format_version(major, minor, patch)

    def set_version(self, version: str) -> None:
        """Set version in pyproject.toml and create VERSION file."""
        # Validate version format
        self.parse_version(version)

        # Update pyproject.toml
        content = self.pyproject_file.read_text()
        new_content = re.sub(
            r'version\s*=\s*["\'][^"\']+["\']', f'version = "{version}"', content
        )
        self.pyproject_file.write_text(new_content)

        # Create VERSION file
        self.version_file.write_text(f"{version}\n")

        print(f"✅ Version updated to {version}")

    def get_version_info(self) -> dict:
        """Get comprehensive version information."""
        version = self.get_current_version()
        major, minor, patch = self.parse_version(version)

        return {
            "version": version,
            "major": major,
            "minor": minor,
            "patch": patch,
            "is_prerelease": False,  # Could be extended for alpha/beta versions
            "build_metadata": None,  # Could be extended for build info
        }


def main():
    """Main CLI interface for version management."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/version.py <command> [args]")
        print("Commands:")
        print("  get                    - Get current version")
        print("  bump <type>            - Bump version (major|minor|patch)")
        print("  set <version>          - Set specific version")
        print("  info                   - Get detailed version info")
        sys.exit(1)

    command = sys.argv[1]
    manager = VersionManager()

    try:
        if command == "get":
            version = manager.get_current_version()
            print(version)

        elif command == "bump":
            if len(sys.argv) < 3:
                print("Usage: python scripts/version.py bump <major|minor|patch>")
                sys.exit(1)
            version_type = sys.argv[2]
            new_version = manager.bump_version(version_type)
            manager.set_version(new_version)

        elif command == "set":
            if len(sys.argv) < 3:
                print("Usage: python scripts/version.py set <version>")
                sys.exit(1)
            version = sys.argv[2]
            manager.set_version(version)

        elif command == "info":
            info = manager.get_version_info()
            print(f"Version: {info['version']}")
            print(f"Major: {info['major']}")
            print(f"Minor: {info['minor']}")
            print(f"Patch: {info['patch']}")
            print(f"Prerelease: {info['is_prerelease']}")

        else:
            print(f"Unknown command: {command}")
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
