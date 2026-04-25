"""Exercise the `messaging_*` MCP tools via an in-process FastMCP Client.

Calls the read verbs (`messaging_list`, `messaging_get`) to show every
tool lands typed shapes on the wire. Writes (`messaging_send`,
`messaging_reply`, `messaging_mark_read`, `messaging_mark_unread`,
`messaging_delete`, `messaging_set_priority`, `messaging_set_status`,
`messaging_assign`, `messaging_unassign`) are in the tool surface —
skipped here because they mutate the shared local stack.

Usage:
    uv run python examples/mcp/messaging.py
"""

from __future__ import annotations

import asyncio
import os

from dhis2_mcp.server import build_server
from fastmcp import Client


async def main() -> None:
    """Connect to the in-process MCP server and call a couple of read tools."""
    profile = os.environ.get("DHIS2_PROFILE", "local_basic")
    async with Client(build_server()) as client:
        listing = await client.call_tool("messaging_list", {"profile": profile, "page_size": 5})
        rows = listing.data or listing.structured_content or []
        print(f"messaging_list returned {len(rows)} rows")

        if rows:
            first_uid = rows[0]["id"] if isinstance(rows[0], dict) else rows[0].id
            convo = await client.call_tool("messaging_get", {"profile": profile, "uid": first_uid})
            payload = convo.data or convo.structured_content
            subject = payload.get("subject") if isinstance(payload, dict) else payload.subject
            print(f"messaging_get({first_uid}) -> subject={subject!r}")


if __name__ == "__main__":
    asyncio.run(main())
