"""End-to-end MCP tests against the local DHIS2 instance via FastMCP's in-process Client."""

from __future__ import annotations

import json

import pytest
from dhis2w_mcp.server import build_server
from fastmcp import Client

pytestmark = pytest.mark.slow


async def test_whoami_tool_returns_admin_user(
    local_url: str, local_pat: str | None, monkeypatch: pytest.MonkeyPatch
) -> None:
    if not local_pat:
        pytest.skip("DHIS2_PAT not set — run `make dhis2-run` to populate")
    monkeypatch.setenv("DHIS2_URL", local_url)
    monkeypatch.setenv("DHIS2_PAT", local_pat)

    server = build_server()
    async with Client(server) as client:
        result = await client.call_tool("system_whoami", {})

    payload = _extract_payload(result)
    assert payload.get("username") == "admin"


async def test_system_info_tool_returns_version(
    local_url: str, local_pat: str | None, monkeypatch: pytest.MonkeyPatch
) -> None:
    if not local_pat:
        pytest.skip("DHIS2_PAT not set — run `make dhis2-run` to populate")
    monkeypatch.setenv("DHIS2_URL", local_url)
    monkeypatch.setenv("DHIS2_PAT", local_pat)

    server = build_server()
    async with Client(server) as client:
        result = await client.call_tool("system_info", {})

    payload = _extract_payload(result)
    version = payload.get("version")
    assert isinstance(version, str)
    assert version.startswith(("2.", "3."))


def _extract_payload(result: object) -> dict[str, object]:
    """FastMCP tool-call results carry a .structured_content or .content field.

    Normalize to a plain dict regardless of FastMCP version.
    """
    structured = getattr(result, "structured_content", None)
    if isinstance(structured, dict):
        return structured
    data = getattr(result, "data", None)
    if data is not None and hasattr(data, "model_dump"):
        dumped = data.model_dump()
        if isinstance(dumped, dict):
            return dumped
    if isinstance(data, dict):
        return data
    content = getattr(result, "content", None)
    if isinstance(content, list) and content:
        first = content[0]
        text = getattr(first, "text", None)
        if isinstance(text, str):
            parsed = json.loads(text)
            if isinstance(parsed, dict):
                return parsed
    raise AssertionError(f"unexpected FastMCP result shape: {result!r}")
