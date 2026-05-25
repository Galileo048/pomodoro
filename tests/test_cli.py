"""Integration tests for the CLI."""

import os
import subprocess
import sys

import pytest


def run_f2m(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [sys.executable, "-m", "formula2manim.cli", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )


class TestCLIBasic:
    def test_dry_run_uniform_acceleration(self):
        result = run_f2m(
            "-f", "x = v0*t + 0.5*a*t**2",
            "-p", "v0=0, a=9.8",
            "--dry-run",
        )
        assert result.returncode == 0, result.stderr
        stdout = result.stdout or ""
        assert "Validation Passed" in stdout

    def test_dry_run_projectile(self):
        result = run_f2m(
            "-f", "x = v0x*t; y = v0y*t - 0.5*g*t**2",
            "-p", "v0x=10, v0y=20, g=9.8",
            "--dry-run",
        )
        assert result.returncode == 0, result.stderr
        stdout = result.stdout or ""
        assert "Validation Passed" in stdout

    def test_missing_formulas(self):
        result = run_f2m("-p", "v0=0")
        assert result.returncode != 0

    def test_missing_params_validation_fails(self):
        """Model validation should fail when params are missing."""
        result = run_f2m("-f", "x = v0*t + 0.5*a*t**2", "-p", "v0=0")
        assert result.returncode != 0

    def test_invalid_model_name(self):
        result = run_f2m(
            "-f", "x = v0*t",
            "-p", "v0=0, a=1",
            "-m", "nonexistent_model",
        )
        assert result.returncode != 0

    def test_describe_without_ai(self):
        result = run_f2m("--describe", "A ball thrown horizontally")
        assert result.returncode != 0
        output = (result.stdout or "") + (result.stderr or "")
        assert "--ai" in output

    def test_version(self):
        result = run_f2m("--version")
        assert result.returncode == 0
        output = result.stdout or ""
        assert "formula2manim" in output

    def test_dry_run_with_model_flag(self):
        result = run_f2m(
            "-f", "x = v0*t + 0.5*a*t**2",
            "-p", "v0=0, a=9.8",
            "-m", "uniform_acceleration",
            "--dry-run",
            "-v",
        )
        assert result.returncode == 0, result.stderr
