"""MCP aggregate tool tests via in-process FastMCP Client against local DHIS2."""

from __future__ import annotations

import json

import pytest
from dhis2_mcp.server import build_server
from fastmcp import Client

pytestmark = pytest.mark.slow


def _extract_payload(result: object) -> object:
    structured = getattr(result, "structured_content", None)
    if structured is not None:
        if isinstance(structured, dict) and "result" in structured:
            return structured["result"]
        return structured
    data = getattr(result, "data", None)
    if data is not None and hasattr(data, "model_dump"):
        return data.model_dump()
    if data is not None:
        return data
    content = getattr(result, "content", None)
    if isinstance(content, list) and content:
        first = content[0]
        text = getattr(first, "text", None)
        if isinstance(text, str):
            return json.loads(text)
    raise AssertionError(f"unexpected FastMCP result shape: {result!r}")


async def test_get_data_values_returns_envelope(
    local_url: str, local_pat: str | None, monkeypatch: pytest.MonkeyPatch
) -> None:
    if not local_pat:
        pytest.skip("DHIS2_PAT not set — run `make dhis2-run` to populate")
    monkeypatch.setenv("DHIS2_URL", local_url)
    monkeypatch.setenv("DHIS2_PAT", local_pat)

    server = build_server()
    async with Client(server) as client:
        datasets = _extract_payload(
            await client.call_tool(
                "list_metadata",
                {"resource": "dataSets", "fields": "id,name", "limit": 1},
            )
        )
        org_units = _extract_payload(
            await client.call_tool(
                "list_metadata",
                {"resource": "organisationUnits", "fields": "id,name", "limit": 1},
            )
        )
        if not (isinstance(datasets, list) and datasets and isinstance(org_units, list) and org_units):
            pytest.skip("instance missing dataSets or organisationUnits")

        result = await client.call_tool(
            "get_data_values",
            {
                "data_set": datasets[0]["id"],
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
                "org_unit": org_units[0]["id"],
                "children": True,
                "limit": 5,
            },
        )

    envelope = _extract_payload(result)
    assert isinstance(envelope, dict)
    assert "dataValues" in envelope
    assert isinstance(envelope["dataValues"], list)


async def test_push_data_values_dry_run(local_url: str, local_pat: str | None, monkeypatch: pytest.MonkeyPatch) -> None:
    if not local_pat:
        pytest.skip("DHIS2_PAT not set — run `make dhis2-run` to populate")
    monkeypatch.setenv("DHIS2_URL", local_url)
    monkeypatch.setenv("DHIS2_PAT", local_pat)

    server = build_server()
    async with Client(server) as client:
        des = _extract_payload(
            await client.call_tool(
                "list_metadata",
                {"resource": "dataElements", "fields": "id,name", "limit": 1},
            )
        )
        ous = _extract_payload(
            await client.call_tool(
                "list_metadata",
                {"resource": "organisationUnits", "fields": "id,name", "limit": 1},
            )
        )
        if not (isinstance(des, list) and des and isinstance(ous, list) and ous):
            pytest.skip("insufficient metadata to form a push payload")

        result = await client.call_tool(
            "push_data_values",
            {
                "data_values": [
                    {
                        "dataElement": des[0]["id"],
                        "orgUnit": ous[0]["id"],
                        "period": "202401",
                        "value": "7",
                    }
                ],
                "dry_run": True,
            },
        )

    response = _extract_payload(result)
    assert isinstance(response, dict)
    assert any(key in response for key in ("status", "httpStatus", "importCount", "response"))
