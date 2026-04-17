"""FastMCP tool registration for the `system` plugin."""

from __future__ import annotations

from typing import Any

from dhis2_client import Me, SystemInfo

from dhis2_core.plugins.system import service
from dhis2_core.profile import profile_from_env


def register(mcp: Any) -> None:
    """Register `whoami` and `system_info` as MCP tools on `mcp`."""

    @mcp.tool()
    async def whoami() -> Me:
        """Return the authenticated DHIS2 user for the current environment profile."""
        return await service.whoami(profile_from_env())

    @mcp.tool()
    async def system_info() -> SystemInfo:
        """Return /api/system/info for the current environment profile."""
        return await service.system_info(profile_from_env())
