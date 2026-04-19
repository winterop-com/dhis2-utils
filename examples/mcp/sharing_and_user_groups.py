"""Sharing + user-group administration via MCP tools.

Read-only agent walkthrough: list user groups, grab one's sharing block,
list user roles + their authorities. Uses the seeded fixture.

Write tools (`user_group_add_member`, `user_role_add_user`,
`user_group_sharing-grant-user` via CLI) exist; the example stays read-only
to avoid hitting real DHIS2 state.

Usage:
    uv run python examples/mcp/sharing_and_user_groups.py
"""

from __future__ import annotations

import asyncio
from typing import Any

from dhis2_mcp.server import build_server
from fastmcp import Client


async def main() -> None:
    """List groups + roles + inspect one sharing block."""

    def _result(response: Any) -> Any:
        """Unwrap the `structured_content` wrapper from a FastMCP call_tool response."""
        payload = response.structured_content or response.data or {}
        if isinstance(payload, dict) and "result" in payload:
            return payload["result"]
        return payload

    server = build_server()
    async with Client(server) as client:
        groups = _result(await client.call_tool("user_group_list", {"fields": "id,displayName,users"})) or []
        print(f"user groups: {len(groups)}")
        for group in groups[:3]:
            members = group.get("users") or []
            print(f"  {group.get('displayName')}  ({group.get('id')})  members={len(members)}")

        if groups:
            first_uid = groups[0].get("id")
            sharing = _result(await client.call_tool("user_group_sharing_get", {"uid": first_uid})) or {}
            print(f"\nsharing for user group {first_uid}:")
            print(f"  publicAccess={sharing.get('publicAccess')}")
            print(f"  userAccesses={len(sharing.get('userAccesses') or [])}")
            print(f"  userGroupAccesses={len(sharing.get('userGroupAccesses') or [])}")

        roles = _result(await client.call_tool("user_role_list", {"fields": "id,displayName,authorities,users"})) or []
        print(f"\nuser roles: {len(roles)}")
        for role in roles[:3]:
            auth_count = len(role.get("authorities") or [])
            print(f"  {role.get('displayName')}  authorities={auth_count}")

        if roles:
            auths = _result(await client.call_tool("user_role_authorities", {"uid": roles[0]["id"]})) or []
            print(f"\nfirst 10 authorities on {roles[0]['displayName']}:")
            for a in auths[:10]:
                print(f"  {a}")


if __name__ == "__main__":
    asyncio.run(main())
