"""MCP analytics tool tests via in-process FastMCP Client against local DHIS2."""

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


async def test_query_analytics_tool(local_url: str, local_pat: str | None, monkeypatch: pytest.MonkeyPatch) -> None:
    if not local_pat:
        pytest.skip("DHIS2_PAT not set — run `make dhis2-run` to populate")
    monkeypatch.setenv("DHIS2_URL", local_url)
    monkeypatch.setenv("DHIS2_PAT", local_pat)

    server = build_server()
    async with Client(server) as client:
        des = _extract_payload(
            await client.call_tool("list_metadata", {"resource": "dataElements", "fields": "id,name", "limit": 1})
        )
        ous = _extract_payload(
            await client.call_tool(
                "list_metadata",
                {
                    "resource": "organisationUnits",
                    "fields": "id,name",
                    "filter": "level:eq:1",
                    "limit": 1,
                },
            )
        )
        if not (isinstance(des, list) and des and isinstance(ous, list) and ous):
            pytest.skip("instance missing required metadata")

        result = await client.call_tool(
            "query_analytics",
            {
                "dimensions": [
                    f"dx:{des[0]['id']}",
                    "pe:LAST_12_MONTHS",
                    f"ou:{ous[0]['id']}",
                ],
                "skip_meta": True,
            },
        )

    payload = _extract_payload(result)
    assert isinstance(payload, dict)
    assert any(key in payload for key in ("headers", "rows", "metaData"))
