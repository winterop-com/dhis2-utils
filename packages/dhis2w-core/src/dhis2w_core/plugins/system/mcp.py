"""FastMCP tool registration for the `system` plugin."""

from __future__ import annotations

from typing import Any

from dhis2w_client import DhisCalendar, Me, SystemInfo

from dhis2w_core.plugins.system import service
from dhis2w_core.profile import resolve_profile


def register(mcp: Any) -> None:
    """Register `system_whoami`, `system_info`, and calendar tools on `mcp`."""

    @mcp.tool()
    async def system_whoami(profile: str | None = None) -> Me:
        """Return the authenticated DHIS2 user.

        `profile` selects a named profile from the project or global
        `profiles.toml`. Omit to use the default (from `DHIS2_PROFILE` env,
        raw `DHIS2_URL/PAT` env, or the TOML `default`).
        """
        return await service.whoami(resolve_profile(profile))

    @mcp.tool()
    async def system_info(profile: str | None = None) -> SystemInfo:
        """Return /api/system/info for the given profile (see `system_whoami` for precedence)."""
        return await service.system_info(resolve_profile(profile))

    @mcp.tool()
    async def system_calendar_get(profile: str | None = None) -> str:
        """Return the active DHIS2 calendar (`keyCalendar`) — `iso8601` by default."""
        return await service.get_calendar(resolve_profile(profile))

    @mcp.tool()
    async def system_calendar_set(calendar: DhisCalendar, profile: str | None = None) -> str:
        """Set the DHIS2 calendar setting and return the value written.

        `calendar` must be one of the canonical DHIS2 calendar names —
        coptic, ethiopian, gregorian, islamic, iso8601, julian, nepali,
        persian, thai. Rarely needs to be changed.
        """
        await service.set_calendar(resolve_profile(profile), calendar)
        return calendar.value
