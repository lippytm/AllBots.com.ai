#!/usr/bin/env python3
"""
ci_cd/run_tests.py
==================
Local test-runner script that mirrors the GitHub Actions bot-testing workflow.

Usage
-----
    python ci_cd/run_tests.py

This script discovers and executes the project test suite, prints a structured
summary, and exits with a non-zero status code on failure so that it can be
called from shell pipelines or CI steps.
"""
from __future__ import annotations

import subprocess
import sys


def main() -> int:
    print("=" * 60)
    print("AllBots.com.ai — Bot Test Suite")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
        check=False,
    )

    if result.returncode == 0:
        print("\n✅  All tests passed.")
    else:
        print("\n❌  Some tests failed. Review output above.")

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
