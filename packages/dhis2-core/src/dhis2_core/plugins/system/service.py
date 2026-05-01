"""Service layer for the `system` plugin — wraps /api/system/info and /api/me."""

from __future__ import annotations

from dhis2_client.system import DhisCalendar, Me, SystemInfo
from pydantic import BaseModel, ConfigDict

from dhis2_core.client_context import open_client
from dhis2_core.profile import Profile


class _SystemIdResponse(BaseModel):
    """Envelope for `GET /api/system/id` — returns `{codes: ["UID", ...]}`."""

    model_config = ConfigDict(extra="allow")

    codes: list[str] = []


async def whoami(profile: Profile) -> Me:
    """Return the authenticated user for the given profile."""
    async with open_client(profile) as client:
        return await client.system.me()


async def system_info(profile: Profile) -> SystemInfo:
    """Return the DHIS2 system info for the given profile."""
    async with open_client(profile) as client:
        return await client.system.info()


async def get_calendar(profile: Profile) -> str:
    """Return the active DHIS2 calendar (`keyCalendar`) for the given profile."""
    async with open_client(profile) as client:
        return await client.system.calendar()


async def set_calendar(profile: Profile, calendar: DhisCalendar | str) -> None:
    """Write the DHIS2 calendar setting for the given profile."""
    async with open_client(profile) as client:
        await client.system.set_calendar(calendar)


async def generate_uids(profile: Profile, *, limit: int = 1) -> list[str]:
    """Generate `limit` fresh DHIS2 UIDs via `/api/system/id`.

    Returns the raw 11-char UIDs — useful for creating metadata with
    caller-chosen ids without writing your own UID generator.
    """
    async with open_client(profile) as client:
        response = await client.get("/api/system/id", model=_SystemIdResponse, params={"limit": limit})
    return response.codes
