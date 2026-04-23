"""Call the `metadata_legend_set_*` MCP tools in-process.

Mirrors `examples/client/legend_sets.py` but via the MCP tool surface:
list → create → show → delete round-trip, no library import needed on
the agent side.

Usage:
    uv run python examples/mcp/legend_sets.py
"""

from __future__ import annotations

import asyncio
import os

from dhis2_mcp.server import build_server
from fastmcp import Client


async def main() -> None:
    """List existing sets, create one via MCP, read it back, delete."""
    profile = os.environ.get("DHIS2_PROFILE", "local_basic")
    async with Client(build_server()) as client:
        listed = await client.call_tool("metadata_legend_set_list", {"profile": profile})
        rows = listed.data or listed.structured_content or []
        print(f"existing legendSets: {len(rows)}")

        created = await client.call_tool(
            "metadata_legend_set_create",
            {
                "name": "MCP demo coverage",
                "code": "MCP_DEMO_COVERAGE",
                "legends": [
                    {"start": 0, "end": 50, "color": "#d73027", "name": "Low"},
                    {"start": 50, "end": 80, "color": "#fdae61", "name": "Medium"},
                    {"start": 80, "end": 120, "color": "#1a9850", "name": "High"},
                ],
                "profile": profile,
            },
        )
        envelope = created.data or created.structured_content or {}
        new_uid = envelope.get("id") if isinstance(envelope, dict) else None
        print(f"created legendSet {new_uid}")

        if new_uid:
            fetched = await client.call_tool("metadata_legend_set_show", {"uid": new_uid, "profile": profile})
            show_env = fetched.data or fetched.structured_content or {}
            legend_count = len((show_env.get("legends") if isinstance(show_env, dict) else []) or [])
            print(f"round-trip: {legend_count} legends read back")

            await client.call_tool("metadata_legend_set_delete", {"uid": new_uid, "profile": profile})
            print(f"deleted legendSet {new_uid}")


if __name__ == "__main__":
    asyncio.run(main())
