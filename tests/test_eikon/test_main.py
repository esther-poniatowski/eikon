"""Tests for eikon.__main__ entry point."""

import subprocess
import sys


class TestMainEntry:
    def test_module_invocation_help(self):
        """python -m eikon --help should succeed."""
        result = subprocess.run(
            [sys.executable, "-m", "eikon", "--help"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0
        assert "eikon" in result.stdout.lower()
