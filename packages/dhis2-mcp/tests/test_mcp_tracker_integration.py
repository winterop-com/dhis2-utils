"""MCP tracker tool tests via in-process FastMCP Client against local DHIS2."""

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


async def test_list_events_tool_reaches_server(
    local_url: str, local_pat: str | None, monkeypatch: pytest.MonkeyPatch
) -> None:
    if not local_pat:
        pytest.skip("DHIS2_PAT not set — run `make dhis2-run` to populate")
    monkeypatch.setenv("DHIS2_URL", local_url)
    monkeypatch.setenv("DHIS2_PAT", local_pat)

    server = build_server()
    async with Client(server) as client:
        programs = _extract_payload(
            await client.call_tool(
                "metadata_list",
                {"resource": "programs", "fields": "id,name,programType", "page_size": 50},
            )
        )
        assert isinstance(programs, list)
        event_programs = [p for p in programs if p.get("programType") == "WITHOUT_REGISTRATION"]
        if not event_programs:
            pytest.skip("no event programs on this instance")

        root_ous = _extract_payload(
            await client.call_tool(
                "metadata_list",
                {"resource": "organisationUnits", "fields": "id,name,level", "filters": ["level:eq:2"], "page_size": 1},
            )
        )
        if not (isinstance(root_ous, list) and root_ous):
            pytest.skip("no root orgUnit")

        result = await client.call_tool(
            "data_tracker_event_list",
            {"program": event_programs[0]["id"], "org_unit": root_ous[0]["id"], "page_size": 5},
        )

    envelope = _extract_payload(result)
    if isinstance(envelope, list):
        assert all(isinstance(entry, dict) for entry in envelope)
    else:
        assert isinstance(envelope, dict)
        assert any(key in envelope for key in ("events", "instances", "page", "pager"))
