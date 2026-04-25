"""Exercise the `user_role_*` MCP tools via an in-process FastMCP Client.

Calls the read verbs (`user_role_list`, `user_role_get`,
`user_role_authorities`) to show every tool lands typed shapes on the
wire. Writes (`user_role_add_user`, `user_role_remove_user`) are in
the tool surface — skipped here because granting / revoking roles
mutates the shared local stack.

Usage:
    uv run python examples/mcp/user_role.py
"""

from __future__ import annotations

import asyncio
import os

from dhis2_mcp.server import build_server
from fastmcp import Client


async def main() -> None:
    """Connect to the in-process MCP server and call a few read tools."""
    profile = os.environ.get("DHIS2_PROFILE", "local_basic")
    async with Client(build_server()) as client:
        listing = await client.call_tool("user_role_list", {"profile": profile, "page_size": 5})
        rows = listing.data or listing.structured_content or []
        print(f"user_role_list returned {len(rows)} rows")

        if rows:
            first_uid = rows[0]["id"] if isinstance(rows[0], dict) else rows[0].id
            role = await client.call_tool("user_role_get", {"profile": profile, "uid": first_uid})
            role_payload = role.data or role.structured_content
            name = role_payload.get("name") if isinstance(role_payload, dict) else role_payload.name
            print(f"user_role_get({first_uid}) -> name={name!r}")

            auths = await client.call_tool("user_role_authorities", {"profile": profile, "uid": first_uid})
            auth_list = auths.data or auths.structured_content or []
            print(f"user_role_authorities({first_uid}) -> {len(auth_list)} authorities")


if __name__ == "__main__":
    asyncio.run(main())
