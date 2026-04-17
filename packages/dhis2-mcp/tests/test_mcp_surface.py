"""Unit tests for dhis2-mcp tool registration via FastMCP's in-process Client."""

from __future__ import annotations

from dhis2_mcp.server import build_server
from fastmcp import Client


async def test_server_registers_expected_tools() -> None:
    server = build_server()
    async with Client(server) as client:
        tools = await client.list_tools()
        names = {t.name for t in tools}
    assert "whoami" in names
    assert "system_info" in names
