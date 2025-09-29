#!/usr/bin/env python3
"""
Build script for creating release packages.
Creates platform-specific executables and distributables.
"""

import shutil
import subprocess
import sys
from pathlib import Path

from version import VersionManager


class ReleaseBuilder:
    """Builds release packages for different platforms."""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path(__file__).parent.parent
        self.dist_dir = self.project_root / "dist"
        self.build_dir = self.project_root / "build"

    def clean_build_dirs(self) -> None:
        """Clean build and dist directories."""
        print("🧹 Cleaning build directories...")

        for dir_path in [self.dist_dir, self.build_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"  ✅ Cleaned {dir_path}")

        # Create fresh directories
        self.dist_dir.mkdir(exist_ok=True)
        self.build_dir.mkdir(exist_ok=True)

    def get_version(self) -> str:
        """Get current version."""
        manager = VersionManager(self.project_root)
        return manager.get_current_version()

    def run_tests(self) -> bool:
        """Run tests before building."""
        print("🧪 Running tests...")

        try:
            result = subprocess.run(
                ["uv", "run", "python", "-m", "pytest", "tests/", "-v"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                print("  ✅ All tests passed")
                return True
            else:
                print(f"  ❌ Tests failed: {result.stderr}")
                return False

        except Exception as e:
            print(f"  ❌ Error running tests: {e}")
            return False

    def build_executable(self, platform: str) -> bool:
        """Build executable for specific platform."""
        print(f"🔨 Building executable for {platform}...")

        try:
            # Use the existing build_tray.py script
            result = subprocess.run(
                ["uv", "run", "python", "scripts/build_tray.py"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                print(f"  ✅ Executable built for {platform}")
                return True
            else:
                print(f"  ❌ Build failed for {platform}: {result.stderr}")
                return False

        except Exception as e:
            print(f"  ❌ Error building for {platform}: {e}")
            return False

    def create_archive(self, platform: str) -> bool:
        """Create archive for platform."""
        print(f"📦 Creating archive for {platform}...")

        try:
            platform_dir = self.dist_dir / platform
            if not platform_dir.exists():
                print(f"  ⚠️  No build directory found for {platform}")
                return False

            # Create archive
            archive_name = f"nia-engineering-portal-{self.get_version()}-{platform}"
            archive_path = self.dist_dir / f"{archive_name}.tar.gz"

            subprocess.run(
                ["tar", "-czf", str(archive_path), "-C", str(self.dist_dir), platform],
                check=True,
            )

            print(f"  ✅ Created {archive_path}")
            return True

        except Exception as e:
            print(f"  ❌ Error creating archive for {platform}: {e}")
            return False

    def create_installer_script(self, platform: str) -> bool:
        """Create installer script for platform."""
        print(f"📝 Creating installer script for {platform}...")

        try:
            installer_content = self._generate_installer_script(platform)
            installer_path = self.dist_dir / f"install-{platform}.sh"

            installer_path.write_text(installer_content)
            installer_path.chmod(0o755)

            print(f"  ✅ Created {installer_path}")
            return True

        except Exception as e:
            print(f"  ❌ Error creating installer script: {e}")
            return False

    def _generate_installer_script(self, platform: str) -> str:
        """Generate installer script content."""
        version = self.get_version()

        return f"""#!/bin/bash
# NIA Engineering Portal Installer for {platform}
# Version: {version}

set -e

echo "🚀 Installing NIA Engineering Portal {version} for {platform}..."

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "❌ This script should not be run as root"
   exit 1
fi

# Create installation directory
INSTALL_DIR="$HOME/.local/share/nia-engineering-portal"
mkdir -p "$INSTALL_DIR"

# Copy files
echo "📦 Installing files..."
cp -r nia-engineering-portal-{version}-{platform}/* "$INSTALL_DIR/"

# Create desktop entry
DESKTOP_ENTRY="$HOME/.local/share/applications/nia-engineering-portal.desktop"
cat > "$DESKTOP_ENTRY" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=NIA Engineering Portal
Comment=Engineering portal for broadcast/AV infrastructure
Exec=$INSTALL_DIR/nia-engineering-portal
Icon=$INSTALL_DIR/icon.png
Terminal=false
Categories=Network;AudioVideo;
StartupNotify=true
EOF

# Make executable
chmod +x "$INSTALL_DIR/nia-engineering-portal"

echo "✅ Installation complete!"
echo "📍 Installed to: $INSTALL_DIR"
echo "🎯 Desktop entry created: $DESKTOP_ENTRY"
echo ""
echo "You can now run the application from your applications menu or by running:"
echo "  $INSTALL_DIR/nia-engineering-portal"
"""

    def create_release_notes(self) -> bool:
        """Create release notes."""
        print("📝 Creating release notes...")

        try:
            version = self.get_version()
            notes_content = f"""# NIA Engineering Portal v{version}

## What's New

- Cross-platform tray application
- Web-based configuration interface
- Comprehensive testing framework
- Performance optimizations
- Accessibility improvements

## Installation

1. Download the appropriate package for your platform
2. Extract the archive
3. Run the installer script: `./install-<platform>.sh`

## Features

- **Tray Application**: System tray integration for easy access
- **Configuration**: Web-based configuration interface
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Performance**: Optimized for fast loading and responsiveness
- **Accessibility**: WCAG compliant interface

## System Requirements

- Python 3.12 or higher
- Modern web browser
- 50MB available disk space

## Support

For issues and questions, please refer to the documentation or contact the development team.
"""

            notes_path = self.dist_dir / "RELEASE_NOTES.md"
            notes_path.write_text(notes_content)

            print(f"  ✅ Created {notes_path}")
            return True

        except Exception as e:
            print(f"  ❌ Error creating release notes: {e}")
            return False

    def build_all(self) -> bool:
        """Build all release packages."""
        print("🚀 Starting release build process...")
        print(f"📋 Version: {self.get_version()}")
        print()

        # Clean build directories
        self.clean_build_dirs()

        # Run tests
        if not self.run_tests():
            print("❌ Tests failed, aborting build")
            return False

        # Build for current platform
        import platform

        current_platform = platform.system().lower()

        # Map platform names for consistency
        platform_mapping = {"darwin": "macos", "windows": "windows", "linux": "linux"}
        build_platform = platform_mapping.get(current_platform, current_platform)

        if not self.build_executable(build_platform):
            print(f"❌ Failed to build for {build_platform}")
            return False

        # Create archive
        if not self.create_archive(build_platform):
            print(f"❌ Failed to create archive for {build_platform}")
            return False

        # Create installer script
        if not self.create_installer_script(build_platform):
            print(f"❌ Failed to create installer script for {build_platform}")
            return False

        # Create release notes
        if not self.create_release_notes():
            print("❌ Failed to create release notes")
            return False

        print()
        print("🎉 Release build complete!")
        print(f"📁 Output directory: {self.dist_dir}")
        print()
        print("Generated files:")
        for file in self.dist_dir.iterdir():
            print(f"  - {file.name}")

        return True


def main():
    """Main entry point."""
    builder = ReleaseBuilder()

    if len(sys.argv) > 1 and sys.argv[1] == "--skip-tests":
        print("⚠️  Skipping tests (--skip-tests flag provided)")
        # Override the test method to always return True
        builder.run_tests = lambda: True

    success = builder.build_all()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
