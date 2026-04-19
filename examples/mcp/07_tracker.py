"""Call the `tracker` MCP tools — discover types, list entities/events.

The seeded e2e fixture ships no tracker programs, so most read calls return
empty results. Set `TET_NAME` + `PROGRAM_UID` + `ORG_UNIT_UID` to hit a
tracker-populated instance (e.g. play.dhis2.org/dev).

Usage:
    uv run python examples/mcp/07_tracker.py
"""

from __future__ import annotations

import asyncio
import os

from dhis2_mcp.server import build_server
from fastmcp import Client


async def main() -> None:
    """Enumerate tracker types, then list entities + events if configured."""
    server = build_server()
    async with Client(server) as client:
        types = await client.call_tool("data_tracker_type_list", {})
        type_payload = types.structured_content or types.data or {}
        type_rows = type_payload.get("result", []) if isinstance(type_payload, dict) else type_payload
        print(f"configured TrackedEntityTypes: {len(type_rows)}")
        for row in type_rows[:5]:
            print(f"  {row.get('id', '?')}  {row.get('name', '?')}")

        program_uid = os.environ.get("PROGRAM_UID")
        tet_name = os.environ.get("TET_NAME")
        if not (program_uid and tet_name and type_rows):
            print("\n(set PROGRAM_UID + TET_NAME to run list/event queries against a real tracker instance)")
            return

        entities = await client.call_tool(
            "data_tracker_list",
            {"tracked_entity_type": tet_name, "program": program_uid, "page_size": 5},
        )
        envelope = entities.structured_content or entities.data or {}
        rows = envelope.get("result", []) if isinstance(envelope, dict) else envelope
        print(f"\nentities ({tet_name} in {program_uid}): {len(rows)}")

        events = await client.call_tool(
            "data_tracker_event_list",
            {"program": program_uid, "page_size": 5},
        )
        envelope = events.structured_content or events.data or {}
        rows = envelope.get("result", []) if isinstance(envelope, dict) else envelope
        print(f"events in {program_uid}: {len(rows)}")


if __name__ == "__main__":
    asyncio.run(main())
