"""End-to-end analytics CLI tests against local DHIS2."""

from __future__ import annotations

import json

import pytest
from dhis2w_cli.main import build_app
from typer.testing import CliRunner

pytestmark = pytest.mark.slow


def _setup_env(monkeypatch: pytest.MonkeyPatch, local_url: str, local_pat: str | None) -> None:
    if not local_pat:
        pytest.skip("DHIS2_PAT not set — run `make dhis2-run` to populate")
    monkeypatch.setenv("DHIS2_URL", local_url)
    monkeypatch.setenv("DHIS2_PAT", local_pat)


def _first_uid(runner: CliRunner, resource: str, extra_args: list[str] | None = None) -> str | None:
    args = ["--json", "metadata", "list", resource, "--fields", "id,name", "--page-size", "1"]
    if extra_args:
        args = args + extra_args
    result = runner.invoke(build_app(), args)
    assert result.exit_code == 0, result.output
    items = json.loads(result.output)
    return str(items[0]["id"]) if items else None


def test_analytics_query_returns_response(
    local_url: str, local_pat: str | None, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Analytics query returns response."""
    _setup_env(monkeypatch, local_url, local_pat)
    runner = CliRunner()
    data_element = _first_uid(runner, "dataElements")
    org_unit = _first_uid(runner, "organisationUnits", ["--filter", "level:eq:1"])
    if not (data_element and org_unit):
        pytest.skip("instance missing required metadata")

    result = runner.invoke(
        build_app(),
        [
            "--json",
            "analytics",
            "query",
            "--dimension",
            f"dx:{data_element}",
            "--dimension",
            "pe:LAST_12_MONTHS",
            "--dimension",
            f"ou:{org_unit}",
            "--skip-meta",
        ],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert any(key in payload for key in ("headers", "rows", "metaData"))
