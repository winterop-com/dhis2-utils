"""End-to-end CLI tests against the local DHIS2 instance, using the seeded PAT."""

from __future__ import annotations

import pytest
from dhis2_cli.main import build_app
from typer.testing import CliRunner

pytestmark = pytest.mark.slow


def test_system_whoami_live(local_url: str, local_pat: str | None, monkeypatch: pytest.MonkeyPatch) -> None:
    if not local_pat:
        pytest.skip("DHIS2_PAT not set — run `make dhis2-run` to populate")
    monkeypatch.setenv("DHIS2_URL", local_url)
    monkeypatch.setenv("DHIS2_PAT", local_pat)
    runner = CliRunner()
    result = runner.invoke(build_app(), ["system", "whoami"])
    assert result.exit_code == 0, result.output
    assert "admin" in result.output


def test_system_info_live(local_url: str, local_pat: str | None, monkeypatch: pytest.MonkeyPatch) -> None:
    if not local_pat:
        pytest.skip("DHIS2_PAT not set — run `make dhis2-run` to populate")
    monkeypatch.setenv("DHIS2_URL", local_url)
    monkeypatch.setenv("DHIS2_PAT", local_pat)
    runner = CliRunner()
    result = runner.invoke(build_app(), ["system", "info"])
    assert result.exit_code == 0, result.output
    assert "version=" in result.output
