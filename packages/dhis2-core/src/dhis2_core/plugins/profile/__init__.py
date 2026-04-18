"""Profile plugin — manage DHIS2 profiles across project and global TOML files."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from dhis2_core.plugins.profile import cli as cli_module
from dhis2_core.plugins.profile import mcp as mcp_module


@dataclass(frozen=True)
class _ProfilePlugin:
    """Plugin descriptor for DHIS2 profile management."""

    name: str = "profile"
    description: str = "List, verify, switch, add, and remove DHIS2 profiles."

    def register_cli(self, app: Any) -> None:
        """Mount under `dhis2 profile`."""
        cli_module.register(app)

    def register_mcp(self, mcp: Any) -> None:
        """Register read-only profile tools on the MCP server."""
        mcp_module.register(mcp)


plugin = _ProfilePlugin()
