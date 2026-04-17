"""Service layer for the `system` plugin — wraps /api/system/info and /api/me."""

from __future__ import annotations

from dhis2_client import Me, SystemInfo

from dhis2_core.client_context import open_client
from dhis2_core.profile import Profile


async def whoami(profile: Profile) -> Me:
    """Return the authenticated user for the given profile."""
    async with open_client(profile) as client:
        return await client.system.me()


async def system_info(profile: Profile) -> SystemInfo:
    """Return the DHIS2 system info for the given profile."""
    async with open_client(profile) as client:
        return await client.system.info()
