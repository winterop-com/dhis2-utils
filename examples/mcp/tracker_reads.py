"""Call the `tracker` MCP tools — discover types, list entities/events.

Targets the seeded Child Programme (IpHINAT79UW, WITH_REGISTRATION) and
the seeded Supervision visit event program (EVTsupVis01,
WITHOUT_REGISTRATION) out of the box. Override via env to point at a
different instance.

For the authoring side (register / enroll / add_event / outstanding),
see `examples/mcp/tracker_workflow.py`.

Usage:
    uv run python examples/mcp/tracker_reads.py

Env (all optional — fall back to seeded Sierra Leone UIDs):
    PROGRAM_UID       default IpHINAT79UW (Child Programme)
    EVENT_PROGRAM_UID default EVTsupVis01 (Supervision visit)
    TET_NAME          default "Person (Play)"
"""

from __future__ import annotations

import asyncio
import os

from dhis2_mcp.server import build_server
from fastmcp import Client


async def main() -> None:
    """Enumerate TETs, list entities + events against both program kinds."""
    program_uid = os.environ.get("PROGRAM_UID", "IpHINAT79UW")
    event_program_uid = os.environ.get("EVENT_PROGRAM_UID", "EVTsupVis01")
    tet_name = os.environ.get("TET_NAME", "Person (Play)")

    server = build_server()
    async with Client(server) as client:
        types = await client.call_tool("data_tracker_type_list", {})
        type_payload = types.structured_content or types.data or {}
        type_rows = type_payload.get("result", []) if isinstance(type_payload, dict) else type_payload
        print(f"configured TrackedEntityTypes: {len(type_rows)}")
        for row in type_rows[:5]:
            print(f"  {row.get('id', '?')}  {row.get('name', '?')}")

        entities = await client.call_tool(
            "data_tracker_list",
            {"tracked_entity_type": tet_name, "program": program_uid, "page_size": 5},
        )
        envelope = entities.structured_content or entities.data or {}
        rows = envelope.get("result", []) if isinstance(envelope, dict) else envelope
        print(f"\nentities ({tet_name} in {program_uid}): {len(rows)}")

        # Tracker-program events
        events = await client.call_tool(
            "data_tracker_event_list",
            {"program": program_uid, "page_size": 5},
        )
        envelope = events.structured_content or events.data or {}
        rows = envelope.get("result", []) if isinstance(envelope, dict) else envelope
        print(f"events in {program_uid} (tracker program): {len(rows)}")

        # Event-program events — same MCP tool, just a different program UID.
        events = await client.call_tool(
            "data_tracker_event_list",
            {"program": event_program_uid, "page_size": 5},
        )
        envelope = events.structured_content or events.data or {}
        rows = envelope.get("result", []) if isinstance(envelope, dict) else envelope
        print(f"events in {event_program_uid} (event program): {len(rows)}")


if __name__ == "__main__":
    asyncio.run(main())
