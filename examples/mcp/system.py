"""Exercise the `system_*` MCP tools via an in-process FastMCP Client.

Calls both read tools (`system_whoami`, `system_info`) — the entire
surface of the system plugin is read-only.

Usage:
    uv run python examples/mcp/system.py
"""

from __future__ import annotations

import asyncio
import os

from dhis2_mcp.server import build_server
from fastmcp import Client


async def main() -> None:
    """Connect to the in-process MCP server and call both read tools."""
    profile = os.environ.get("DHIS2_PROFILE", "local_basic")
    async with Client(build_server()) as client:
        me = await client.call_tool("system_whoami", {"profile": profile})
        me_payload = me.data or me.structured_content
        username = me_payload.get("username") if isinstance(me_payload, dict) else me_payload.username
        print(f"system_whoami -> username={username!r}")

        info = await client.call_tool("system_info", {"profile": profile})
        info_payload = info.data or info.structured_content
        version = info_payload.get("version") if isinstance(info_payload, dict) else info_payload.version
        print(f"system_info -> version={version!r}")


if __name__ == "__main__":
    asyncio.run(main())
