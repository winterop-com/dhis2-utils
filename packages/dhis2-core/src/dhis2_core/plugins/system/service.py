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


async def generate_uids(profile: Profile, *, limit: int = 1) -> list[str]:
    """Mint `limit` fresh DHIS2 UIDs via `/api/system/id`.

    Returns the raw 11-char UIDs — useful for creating metadata with
    caller-chosen ids without writing your own UID generator.
    """
    async with open_client(profile) as client:
        response = await client.get_raw("/api/system/id", params={"limit": limit})
    codes = response.get("codes")
    if not isinstance(codes, list):
        raise RuntimeError(f"unexpected /api/system/id response: {response!r}")
    return [str(c) for c in codes]
