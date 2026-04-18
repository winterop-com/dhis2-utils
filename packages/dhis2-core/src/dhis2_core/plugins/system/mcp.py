"""FastMCP tool registration for the `system` plugin."""

from __future__ import annotations

from typing import Any

from dhis2_client import Me, SystemInfo

from dhis2_core.plugins.system import service
from dhis2_core.profile import resolve_profile


def register(mcp: Any) -> None:
    """Register `whoami` and `system_info` as MCP tools on `mcp`."""

    @mcp.tool()
    async def whoami(profile: str | None = None) -> Me:
        """Return the authenticated DHIS2 user.

        `profile` selects a named profile from the project or global
        `profiles.toml`. Omit to use the default (from `DHIS2_PROFILE` env,
        raw `DHIS2_URL/PAT` env, or the TOML `default`).
        """
        return await service.whoami(resolve_profile(profile))

    @mcp.tool()
    async def system_info(profile: str | None = None) -> SystemInfo:
        """Return /api/system/info for the given profile (see `whoami` for precedence)."""
        return await service.system_info(resolve_profile(profile))
