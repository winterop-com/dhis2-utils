"""System plugin — exposes /api/system/info and /api/me as CLI + MCP surfaces."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from dhis2_core.plugins.system import cli as cli_module
from dhis2_core.plugins.system import mcp as mcp_module


@dataclass(frozen=True)
class _SystemPlugin:
    """Plugin descriptor for the system capability."""

    name: str = "system"
    description: str = "DHIS2 system info and current-user access."

    def register_cli(self, app: Any) -> None:
        """Mount the system sub-app under `dhis2 system`."""
        cli_module.register(app)

    def register_mcp(self, mcp: Any) -> None:
        """Register `whoami` and `system_info` as MCP tools."""
        mcp_module.register(mcp)


plugin = _SystemPlugin()
