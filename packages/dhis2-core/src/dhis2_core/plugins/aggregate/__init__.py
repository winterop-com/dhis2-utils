"""Aggregate data-values plugin — CLI + MCP wrappers over /api/dataValueSets and /api/dataValues."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from dhis2_core.plugins.aggregate import cli as cli_module
from dhis2_core.plugins.aggregate import mcp as mcp_module


@dataclass(frozen=True)
class _AggregatePlugin:
    """Plugin descriptor for DHIS2 aggregate data values."""

    name: str = "aggregate"
    description: str = "Query and write DHIS2 aggregate data values (bulk + single)."

    def register_cli(self, app: Any) -> None:
        """Mount under `dhis2 aggregate`."""
        cli_module.register(app)

    def register_mcp(self, mcp: Any) -> None:
        """Register get/push/set/delete data-value tools on the MCP server."""
        mcp_module.register(mcp)


plugin = _AggregatePlugin()
