"""Call the `aggregate` MCP tools — GET / SET / DELETE a data value.

Mirrors examples/client/03_push_data_value.py but via the MCP server.

Usage:
    uv run python examples/mcp/06_aggregate.py
"""

from __future__ import annotations

import asyncio

from dhis2_mcp.server import build_server
from fastmcp import Client


async def main() -> None:
    """Read, set, read-back, delete — one aggregate data value."""
    server = build_server()
    async with Client(server) as client:
        before = await client.call_tool(
            "data_aggregate_get",
            {"data_set": "NORMonthDS1", "period": "202603", "org_unit": "NOROsloProv"},
        )
        envelope = before.structured_content or before.data or {}
        rows = envelope.get("dataValues", [])
        print(f"before: {len(rows)} data values for 202603")

        await client.call_tool(
            "data_aggregate_set",
            {
                "data_element": "DEancVisit1",
                "period": "202603",
                "org_unit": "NOROsloProv",
                "value": "77",
            },
        )
        print("set     DEancVisit1 / 202603 / NOROsloProv = 77")

        after = await client.call_tool(
            "data_aggregate_get",
            {"data_set": "NORMonthDS1", "period": "202603", "org_unit": "NOROsloProv"},
        )
        envelope = after.structured_content or after.data or {}
        print(f"after:  {len(envelope.get('dataValues', []))} data values for 202603")

        await client.call_tool(
            "data_aggregate_delete",
            {"data_element": "DEancVisit1", "period": "202603", "org_unit": "NOROsloProv"},
        )
        print("delete  DEancVisit1 / 202603 / NOROsloProv")


if __name__ == "__main__":
    asyncio.run(main())
