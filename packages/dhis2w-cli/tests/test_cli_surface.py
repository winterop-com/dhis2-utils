"""Unit tests for the dhis2 CLI root and plugin-mounted sub-apps."""

from __future__ import annotations

from dhis2w_cli.main import build_app
from typer.testing import CliRunner


def test_help_lists_discovered_plugins() -> None:
    """Help lists discovered plugins."""
    runner = CliRunner()
    result = runner.invoke(build_app(), ["--help"])
    assert result.exit_code == 0
    for name in ("analytics", "data", "dev", "metadata", "profile", "route", "system"):
        assert name in result.stdout


def test_system_subcommand_help_lists_commands() -> None:
    """System subcommand help lists commands."""
    runner = CliRunner()
    result = runner.invoke(build_app(), ["system", "--help"])
    assert result.exit_code == 0
    assert "whoami" in result.stdout
    assert "info" in result.stdout


def test_data_subcommand_tree() -> None:
    """Data subcommand tree."""
    runner = CliRunner()
    data_help = runner.invoke(build_app(), ["data", "--help"])
    assert data_help.exit_code == 0
    assert "aggregate" in data_help.stdout
    assert "tracker" in data_help.stdout
    tracker_help = runner.invoke(build_app(), ["data", "tracker", "--help"])
    assert tracker_help.exit_code == 0
    for sub in ("entity", "enrollment", "event", "relationship", "push"):
        assert sub in tracker_help.stdout


def test_dev_includes_codegen_and_uid() -> None:
    """Dev includes codegen and uid."""
    runner = CliRunner()
    result = runner.invoke(build_app(), ["dev", "--help"])
    assert result.exit_code == 0
    for name in ("codegen", "uid", "oauth2"):
        assert name in result.stdout
