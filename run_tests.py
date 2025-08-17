#!/usr/bin/env python3
"""
Test runner for AgriSaarthi project.
Run all tests or specific test categories from the project root.
"""

import sys
import os
import subprocess
from pathlib import Path


def run_test_file(test_file: str) -> bool:
    """Run a specific test file and return success status."""
    try:
        print(f"🧪 Running {test_file}...")

        # Set PYTHONPATH to include current directory
        env = os.environ.copy()
        env["PYTHONPATH"] = str(Path.cwd())

        # Run test from project root
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
            env=env,
        )

        if result.returncode == 0:
            print(f"✅ {test_file} PASSED")
            return True
        else:
            print(f"❌ {test_file} FAILED")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Failed to run {test_file}: {e}")
        return False


def run_all_tests() -> None:
    """Run all test files in the tests directory."""
    print("🌾 AgriSaarthi Test Suite")
    print("=" * 50)

    # Get all test files
    test_files = [
        "tests/test_agents.py",
        "tests/test_all_agents.py",
        "tests/test_markdown.py",
    ]

    passed = 0
    total = len(test_files)

    for test_file in test_files:
        if run_test_file(test_file):
            passed += 1
        print()

    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! The system is working correctly.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)


def run_specific_test(test_name: str) -> None:
    """Run a specific test by name."""
    test_file = f"tests/test_{test_name}.py"

    if not os.path.exists(test_file):
        print(f"❌ Test file {test_file} not found")
        print("Available tests:")
        print("  - agents (test_agents.py)")
        print("  - all_agents (test_all_agents.py)")
        print("  - markdown (test_markdown.py)")
        sys.exit(1)

    success = run_test_file(test_file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific test
        test_name = sys.argv[1]
        run_specific_test(test_name)
    else:
        # Run all tests
        run_all_tests()
