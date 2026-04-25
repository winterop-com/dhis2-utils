"""Exercise the `files_*` MCP tools via an in-process FastMCP Client.

Calls the read verbs (`files_documents_list`, `files_documents_get`)
to show every tool lands typed shapes on the wire. Writes
(`files_documents_create_external`, `files_documents_delete`,
`files_resources_get`) are in the tool surface — skipped here because
mutating the shared local stack is disruptive.

Usage:
    uv run python examples/mcp/files.py
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
        listing = await client.call_tool("files_documents_list", {"profile": profile, "page_size": 5})
        rows = listing.data or listing.structured_content or []
        print(f"files_documents_list returned {len(rows)} rows")

        if rows:
            first_uid = rows[0]["id"] if isinstance(rows[0], dict) else rows[0].id
            doc = await client.call_tool("files_documents_get", {"profile": profile, "uid": first_uid})
            payload = doc.data or doc.structured_content
            print(f"files_documents_get({first_uid}) -> name={payload.get('name') if isinstance(payload, dict) else payload.name}")


if __name__ == "__main__":
    asyncio.run(main())
