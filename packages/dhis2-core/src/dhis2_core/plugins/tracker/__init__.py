"""Tracker plugin — CLI + MCP wrappers over /api/tracker/*."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from dhis2_core.plugins.tracker import cli as cli_module
from dhis2_core.plugins.tracker import mcp as mcp_module


@dataclass(frozen=True)
class _TrackerPlugin:
    """Plugin descriptor for the DHIS2 tracker API."""

    name: str = "tracker"
    description: str = "DHIS2 tracker (tracked entities, enrollments, events, relationships, bulk import)."

    def register_cli(self, app: Any) -> None:
        """Mount under `dhis2 tracker`."""
        cli_module.register(app)

    def register_mcp(self, mcp: Any) -> None:
        """Register tracker tools on the MCP server."""
        mcp_module.register(mcp)


plugin = _TrackerPlugin()
