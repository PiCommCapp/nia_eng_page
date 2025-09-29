#!/usr/bin/env python3
"""
Test runner for the NIA Engineering Portal test suite.
"""

import subprocess
import sys
from pathlib import Path


def run_tests(test_type: str = "all", verbose: bool = True) -> int:
    """Run tests with specified type and verbosity.

    Args:
        test_type: Type of tests to run ('unit', 'integration', 'e2e', 'performance', 'accessibility', 'all')
        verbose: Whether to run with verbose output

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    # Get the project root directory
    project_root = Path(__file__).parent.parent

    # Build pytest command
    cmd = ["python", "-m", "pytest"]

    if verbose:
        cmd.append("-v")

    # Add test type specific options
    if test_type == "unit":
        cmd.extend(["-k", "not (integration or e2e or performance or accessibility)"])
    elif test_type == "integration":
        cmd.extend(["-k", "integration"])
    elif test_type == "e2e":
        cmd.extend(["-k", "e2e"])
    elif test_type == "performance":
        cmd.extend(["-k", "performance"])
    elif test_type == "accessibility":
        cmd.extend(["-k", "accessibility"])
    elif test_type == "all":
        pass  # Run all tests
    else:
        print(f"Unknown test type: {test_type}")
        return 1

    # Add test directory
    cmd.append(str(project_root / "tests"))

    # Add coverage if available
    try:
        import coverage  # noqa: F401

        cmd.extend(
            [
                "--cov=tray_app",
                "--cov=scripts",
                "--cov-report=html",
                "--cov-report=term",
            ]
        )
    except ImportError:
        print("Coverage not available, running without coverage")

    # Run tests
    print(f"Running {test_type} tests...")
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=project_root)
    return result.returncode


def main():
    """Main entry point for test runner."""
    if len(sys.argv) > 1:
        test_type = sys.argv[1]
    else:
        test_type = "all"

    verbose = "-v" in sys.argv or "--verbose" in sys.argv

    exit_code = run_tests(test_type, verbose)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
