"""Unit tests for the dhis2 CLI root and plugin-mounted sub-apps."""

from __future__ import annotations

from dhis2_cli.main import build_app
from typer.testing import CliRunner


def test_help_lists_discovered_plugins() -> None:
    runner = CliRunner()
    result = runner.invoke(build_app(), ["--help"])
    assert result.exit_code == 0
    assert "system" in result.stdout
    assert "codegen" in result.stdout


def test_system_subcommand_help_lists_commands() -> None:
    runner = CliRunner()
    result = runner.invoke(build_app(), ["system", "--help"])
    assert result.exit_code == 0
    assert "whoami" in result.stdout
    assert "info" in result.stdout
