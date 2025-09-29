# NIA Engineering Portal - Deployment Guide

## Overview

This document describes the deployment and release process for the NIA Engineering Portal, including version management, automated builds, and GitHub Actions workflows.

## Version Management

### Current Version

The current version is managed in `pyproject.toml` and can be controlled using the version management script.

### Version Commands

```bash
# Get current version
make version

# Bump version (patch, minor, major)
make version-bump TYPE=patch
make version-bump TYPE=minor
make version-bump TYPE=major

# Set specific version
make version-set VERSION=1.2.3

# Show detailed version info
make version-info
```

### Version Bumping Rules

- **Patch** (0.1.1 → 0.1.2): Bug fixes, minor improvements
- **Minor** (0.1.1 → 0.2.0): New features, enhancements
- **Major** (0.1.1 → 1.0.0): Breaking changes, major rewrites

## Release Process

### Manual Release (GitHub Actions)

1. Go to the GitHub Actions tab
2. Select "Release" workflow
3. Click "Run workflow"
4. Choose version bump type:
   - **patch**: Bug fixes and minor improvements
   - **minor**: New features and enhancements
   - **major**: Breaking changes
5. Optionally skip tests for emergency releases
6. Click "Run workflow"

The workflow will:

- Bump the version automatically
- Run all tests (unless skipped)
- Build release packages
- Create a GitHub release with artifacts
- Commit the version bump to the repository

### Local Release Build

```bash
# Build release packages (with tests)
make release-build

# Build release packages (skip tests for faster builds)
make release-build-fast

# Clean release artifacts
make release-clean
```

### Release Artifacts

Each release includes:

- Platform-specific executables
- Installation scripts
- Release notes
- Source code archives

## GitHub Actions Workflows

### 1. Release Workflow (`.github/workflows/release.yml`)

**Trigger**: Manual (workflow_dispatch)
**Purpose**: Create official releases

**Features**:

- Version bumping (patch/minor/major)
- Optional test skipping for emergency releases
- Automated GitHub release creation
- Artifact upload and tagging

### 2. Build Matrix (`.github/workflows/build-matrix.yml`)

**Trigger**: Push to main/develop, PRs, manual
**Purpose**: Build on multiple platforms

**Platforms**:

- Ubuntu (Linux)
- Windows
- macOS

**Features**:

- Cross-platform testing
- Artifact generation
- Build verification

### 3. Continuous Integration (`.github/workflows/ci.yml`)

**Trigger**: Push to main/develop, PRs
**Purpose**: Code quality and testing

**Features**:

- Linting and formatting checks
- Comprehensive test suite
- Type checking
- Security scanning
- Coverage reporting

### 4. Auto Version Bump (`.github/workflows/auto-version.yml`)

**Trigger**: Push to main (with commit message analysis)
**Purpose**: Automatic version bumping

**Rules**:

- `feat:` commits → minor bump
- `BREAKING CHANGE:` or `feat()!:` → major bump
- Other commits → patch bump
- Skip with `[skip version]` in commit message

## Build Process

### Prerequisites

- Python 3.12+
- UV package manager
- Platform-specific build tools

### Build Steps

1. **Clean**: Remove old build artifacts
2. **Test**: Run comprehensive test suite
3. **Build**: Create platform-specific executables
4. **Package**: Create distribution archives
5. **Document**: Generate release notes

### Build Artifacts

```
dist/
├── linux/
│   ├── nia-engineering-portal
│   └── icon.png
├── windows/
│   ├── nia-engineering-portal.exe
│   └── icon.png
├── macos/
│   ├── nia-engineering-portal
│   └── icon.png
├── nia-engineering-portal-0.1.1-linux.tar.gz
├── nia-engineering-portal-0.1.1-windows.tar.gz
├── nia-engineering-portal-0.1.1-macos.tar.gz
├── install-linux.sh
├── install-windows.sh
├── install-macos.sh
└── RELEASE_NOTES.md
```

## Installation Scripts

### Linux/macOS Installation

```bash
# Download and extract
tar -xzf nia-engineering-portal-0.1.1-linux.tar.gz
cd nia-engineering-portal-0.1.1-linux

# Run installer
./install-linux.sh
```

### Windows Installation

```powershell
# Download and extract
Expand-Archive nia-engineering-portal-0.1.1-windows.zip
cd nia-engineering-portal-0.1.1-windows

# Run installer
.\install-windows.ps1
```

## Release Notes

Release notes are automatically generated and include:

- Version information
- New features and improvements
- Installation instructions
- System requirements
- Support information

## Troubleshooting

### Common Issues

1. **Build Failures**

   - Check Python version (3.12+ required)
   - Verify UV installation
   - Run tests locally before building

2. **Version Conflicts**

   - Ensure version format is semantic (x.y.z)
   - Check for uncommitted changes
   - Verify Git configuration

3. **GitHub Actions Failures**
   - Check workflow logs for specific errors
   - Verify repository permissions
   - Ensure secrets are properly configured

### Debug Commands

```bash
# Check version status
make version-info

# Run tests locally
make test

# Build locally
make release-build

# Check Git status
git status
git log --oneline -5
```

## Security Considerations

- All releases are built in isolated GitHub Actions runners
- Dependencies are locked and verified
- Security scanning is performed on all builds
- Artifacts are signed and verified

## Support

For deployment issues:

1. Check the GitHub Actions logs
2. Review this documentation
3. Contact the development team
4. Create an issue in the repository

## Future Enhancements

- [ ] Automated security updates
- [ ] Docker container builds
- [ ] Package manager distributions (Homebrew, Chocolatey)
- [ ] Automated dependency updates
- [ ] Release rollback capabilities
- [ ] Multi-architecture builds (ARM, x86)
