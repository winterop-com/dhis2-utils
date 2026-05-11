"""End-to-end aggregate CLI tests against local DHIS2."""

from __future__ import annotations

import json
import secrets

import pytest
from dhis2w_cli.main import build_app
from typer.testing import CliRunner

pytestmark = pytest.mark.slow


def _setup_env(monkeypatch: pytest.MonkeyPatch, local_url: str, local_pat: str | None) -> None:
    if not local_pat:
        pytest.skip("DHIS2_PAT not set — run `make dhis2-run` to populate")
    monkeypatch.setenv("DHIS2_URL", local_url)
    monkeypatch.setenv("DHIS2_PAT", local_pat)


def _first_uid(runner: CliRunner, resource: str) -> str | None:
    result = runner.invoke(
        build_app(),
        ["--json", "metadata", "list", resource, "--fields", "id,name", "--page-size", "1"],
    )
    assert result.exit_code == 0, result.output
    items = json.loads(result.output)
    if not items:
        return None
    uid = items[0].get("id")
    return str(uid) if uid else None


def test_aggregate_get_returns_envelope(local_url: str, local_pat: str | None, monkeypatch: pytest.MonkeyPatch) -> None:
    """Aggregate get returns envelope."""
    _setup_env(monkeypatch, local_url, local_pat)
    runner = CliRunner()
    data_set = _first_uid(runner, "dataSets")
    org_unit = _first_uid(runner, "organisationUnits")
    if not (data_set and org_unit):
        pytest.skip("instance missing dataSets or organisationUnits")

    result = runner.invoke(
        build_app(),
        [
            "--json",
            "data",
            "aggregate",
            "get",
            "--data-set",
            data_set,
            "--start-date",
            "2024-01-01",
            "--end-date",
            "2024-01-31",
            "--org-unit",
            org_unit,
            "--children",
            "--limit",
            "5",
        ],
    )
    assert result.exit_code == 0, result.output
    envelope = json.loads(result.output)
    assert "dataValues" in envelope
    assert isinstance(envelope["dataValues"], list)


def test_aggregate_push_dry_run(
    local_url: str, local_pat: str | None, monkeypatch: pytest.MonkeyPatch, tmp_path: object
) -> None:
    """Aggregate push dry run."""
    _setup_env(monkeypatch, local_url, local_pat)
    runner = CliRunner()

    # Discover a dataElement + orgUnit to avoid hard-coding instance-specific UIDs.
    des_result = runner.invoke(
        build_app(),
        ["--json", "metadata", "list", "dataElements", "--fields", "id,name", "--page-size", "1"],
    )
    assert des_result.exit_code == 0, des_result.output
    data_elements = json.loads(des_result.output)
    if not data_elements:
        pytest.skip("no dataElements on the instance")

    ous_result = runner.invoke(
        build_app(),
        ["--json", "metadata", "list", "organisationUnits", "--fields", "id,name", "--page-size", "1"],
    )
    assert ous_result.exit_code == 0, ous_result.output
    org_units = json.loads(ous_result.output)
    if not org_units:
        pytest.skip("no organisationUnits on the instance")

    import_payload = {
        "dataValues": [
            {
                "dataElement": data_elements[0]["id"],
                "orgUnit": org_units[0]["id"],
                "period": "202401",
                "value": str(secrets.randbelow(10) + 1),
            }
        ]
    }
    import_file = tmp_path / "values.json"  # type: ignore[operator]
    import_file.write_text(json.dumps(import_payload))

    result = runner.invoke(
        build_app(),
        ["--json", "data", "aggregate", "push", str(import_file), "--dry-run"],
    )
    assert result.exit_code == 0, result.output
    response = json.loads(result.output)
    # DHIS2 dry-run response always includes a status/httpStatus or importCount summary
    assert any(key in response for key in ("status", "httpStatus", "importCount", "response"))
