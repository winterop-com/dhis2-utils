"""Tests for `client.maintenance.iter_integrity_issues` + `get_integrity_report`."""

from __future__ import annotations

from typing import Any

import httpx
import pytest
import respx
from dhis2_client.auth.basic import BasicAuth
from dhis2_client.client import Dhis2Client
from dhis2_client.maintenance import IntegrityIssueRow


def _details_response(payload: dict[str, Any]) -> httpx.Response:
    """Build a `/api/dataIntegrity/details` response from a `{check_name: result}` dict."""
    return httpx.Response(200, json=payload)


def _mock_connect_preamble() -> None:
    """Stub the canonical-URL + /api/system/info probes `Dhis2Client.connect()` performs."""
    respx.get("https://dhis2.example/").mock(return_value=httpx.Response(200, text="ok"))
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.42.4"}),
    )


_TWO_CHECKS_WITH_ISSUES: dict[str, Any] = {
    "categories_no_options": {
        "name": "categories_no_options",
        "displayName": "Categories without options",
        "severity": "WARNING",
        "count": 2,
        "issues": [
            {"id": "catAAA000001", "name": "Unused Category"},
            {"id": "catBBB000002", "name": "Legacy Category"},
        ],
    },
    "orgunits_no_coordinates": {
        "name": "orgunits_no_coordinates",
        "displayName": "Org units without coordinates",
        "severity": "INFO",
        "count": 1,
        "issues": [
            {"id": "ouAAA0000001", "name": "Lonely OU"},
        ],
    },
}


@respx.mock
async def test_iter_integrity_issues_yields_tagged_rows() -> None:
    """Each issue yields as a typed `IntegrityIssueRow` with the owning check's metadata."""
    _mock_connect_preamble()
    respx.get("https://dhis2.example/api/dataIntegrity/details").mock(
        return_value=_details_response(_TWO_CHECKS_WITH_ISSUES),
    )

    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="a", password="b"))
    try:
        await client.connect()
        rows: list[IntegrityIssueRow] = []
        async for row in client.maintenance.iter_integrity_issues():
            rows.append(row)
    finally:
        await client.close()

    assert len(rows) == 3
    # Stable order: checks in dict-insertion order, issues in list order.
    assert [r.check_name for r in rows] == [
        "categories_no_options",
        "categories_no_options",
        "orgunits_no_coordinates",
    ]
    assert [r.issue.id for r in rows] == ["catAAA000001", "catBBB000002", "ouAAA0000001"]
    assert rows[0].check_display_name == "Categories without options"
    assert rows[0].severity == "WARNING"
    assert rows[2].severity == "INFO"


@respx.mock
async def test_iter_integrity_issues_narrows_with_checks_param() -> None:
    """Passing `checks=[...]` forwards a `?checks=a&checks=b` query to DHIS2."""
    _mock_connect_preamble()
    route = respx.get("https://dhis2.example/api/dataIntegrity/details").mock(
        return_value=_details_response(_TWO_CHECKS_WITH_ISSUES),
    )

    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="a", password="b"))
    try:
        await client.connect()
        rows = [
            row
            async for row in client.maintenance.iter_integrity_issues(
                checks=["categories_no_options", "orgunits_no_coordinates"],
            )
        ]
    finally:
        await client.close()

    assert len(rows) == 3
    params = route.calls.last.request.url.params
    check_params = params.get_list("checks")
    assert check_params == ["categories_no_options", "orgunits_no_coordinates"]


@respx.mock
async def test_iter_integrity_issues_supports_early_break() -> None:
    """Caller can break mid-stream — not a guarantee-of-memory test, but an API-shape test."""
    _mock_connect_preamble()
    respx.get("https://dhis2.example/api/dataIntegrity/details").mock(
        return_value=_details_response(_TWO_CHECKS_WITH_ISSUES),
    )

    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="a", password="b"))
    try:
        await client.connect()
        collected: list[IntegrityIssueRow] = []
        async for row in client.maintenance.iter_integrity_issues():
            collected.append(row)
            if len(collected) == 1:
                break
    finally:
        await client.close()

    assert len(collected) == 1
    assert collected[0].issue.id == "catAAA000001"


@respx.mock
async def test_iter_integrity_issues_empty_when_no_checks_have_run() -> None:
    """DHIS2 returns `{}` when no run has produced details yet — iterator yields nothing, no errors."""
    _mock_connect_preamble()
    respx.get("https://dhis2.example/api/dataIntegrity/details").mock(
        return_value=_details_response({}),
    )

    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="a", password="b"))
    try:
        await client.connect()
        rows = [row async for row in client.maintenance.iter_integrity_issues()]
    finally:
        await client.close()

    assert rows == []


@respx.mock
async def test_get_integrity_report_details_populates_issues() -> None:
    """`get_integrity_report(details=True)` returns the typed report with issues arrays."""
    _mock_connect_preamble()
    respx.get("https://dhis2.example/api/dataIntegrity/details").mock(
        return_value=_details_response(_TWO_CHECKS_WITH_ISSUES),
    )

    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="a", password="b"))
    try:
        await client.connect()
        report = await client.maintenance.get_integrity_report(details=True)
    finally:
        await client.close()

    assert set(report.results) == {"categories_no_options", "orgunits_no_coordinates"}
    assert len(report.results["categories_no_options"].issues) == 2
    assert report.results["categories_no_options"].severity == "WARNING"


@respx.mock
async def test_get_integrity_report_summary_hits_summary_endpoint() -> None:
    """`details=False` uses `/api/dataIntegrity/summary` (cheaper — just counts + timing)."""
    _mock_connect_preamble()
    summary_route = respx.get("https://dhis2.example/api/dataIntegrity/summary").mock(
        return_value=_details_response(
            {
                "categories_no_options": {"name": "categories_no_options", "count": 42, "severity": "WARNING"},
            }
        ),
    )

    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="a", password="b"))
    try:
        await client.connect()
        report = await client.maintenance.get_integrity_report(details=False)
    finally:
        await client.close()

    assert summary_route.called
    assert report.results["categories_no_options"].count == 42
    assert report.results["categories_no_options"].issues == []


def test_integrity_issue_row_is_frozen() -> None:
    """`IntegrityIssueRow` is immutable — no accidental mutation after the iterator yielded it."""
    from dhis2_client.generated.v42.oas import DataIntegrityIssue

    row = IntegrityIssueRow(
        check_name="check",
        check_display_name="Check",
        severity="WARNING",
        issue=DataIntegrityIssue(id="x", name="X"),
    )
    with pytest.raises(Exception):  # pydantic.ValidationError on frozen model  # noqa: B017
        row.check_name = "other"
