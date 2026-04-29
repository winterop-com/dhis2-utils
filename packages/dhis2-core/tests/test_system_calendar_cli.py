"""CliRunner tests for `dhis2 system calendar` (read + write)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
from dhis2_cli.main import build_app
from typer.testing import CliRunner


@pytest.fixture
def pat_profile(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Write a global profiles.toml with one PAT profile and point resolution at it."""
    config_dir = tmp_path / ".config" / "dhis2"
    config_dir.mkdir(parents=True)
    profiles = config_dir / "profiles.toml"
    profiles.write_text(
        """
default = "probe"

[profiles.probe]
base_url = "https://dhis2.example"
auth = "pat"
token = "d2p_test"
"""
    )
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(config_dir.parent))
    monkeypatch.delenv("DHIS2_PROFILE", raising=False)
    monkeypatch.chdir(tmp_path)


def test_calendar_no_arg_prints_current_value(pat_profile: None) -> None:  # noqa: ARG001
    """`dhis2 system calendar` with no arg routes to `service.get_calendar` and prints the value."""
    with patch("dhis2_core.plugins.system.service.get_calendar", new=AsyncMock(return_value="ethiopian")):
        runner = CliRunner()
        result = runner.invoke(build_app(), ["system", "calendar"])
    assert result.exit_code == 0, result.output
    assert "ethiopian" in result.output


def test_calendar_with_arg_writes_setting(pat_profile: None) -> None:  # noqa: ARG001
    """`dhis2 system calendar nepali` routes to `service.set_calendar` with the enum value."""
    set_mock = AsyncMock(return_value=None)
    with patch("dhis2_core.plugins.system.service.set_calendar", new=set_mock):
        runner = CliRunner()
        result = runner.invoke(build_app(), ["system", "calendar", "nepali"])
    assert result.exit_code == 0, result.output
    assert "keyCalendar set to nepali" in result.output
    set_mock.assert_awaited_once()
    assert set_mock.await_args is not None
    _, calendar_arg = set_mock.await_args.args
    assert calendar_arg.value == "nepali"


def test_calendar_rejects_unknown_value(pat_profile: None) -> None:  # noqa: ARG001
    """An unknown calendar name fails with a non-zero exit (Typer enum validation)."""
    runner = CliRunner()
    result = runner.invoke(build_app(), ["system", "calendar", "mayan"])
    assert result.exit_code != 0
