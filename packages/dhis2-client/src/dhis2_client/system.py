"""Typed accessors for /api/system/info and /api/me (non-metadata system endpoints)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from dhis2_client.client import Dhis2Client


class SystemInfo(BaseModel):
    """Shape of `/api/system/info` (common fields; unknown fields preserved)."""

    model_config = ConfigDict(extra="allow")

    version: str | None = None
    revision: str | None = None
    buildTime: str | None = None
    serverDate: str | None = None
    contextPath: str | None = None
    calendar: str | None = None
    dateFormat: str | None = None
    systemId: str | None = None
    systemName: str | None = None


class Me(BaseModel):
    """Shape of `/api/me` for the authenticated user (common fields; unknown preserved)."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None
    username: str | None = None
    displayName: str | None = None
    email: str | None = None
    firstName: str | None = None
    surname: str | None = None
    authorities: list[str] | None = None
    organisationUnits: list[dict[str, Any]] | None = None


class SystemModule:
    """Accessor bound to a `Dhis2Client` exposing system-level endpoints."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def info(self) -> SystemInfo:
        """Fetch `/api/system/info` and return a typed `SystemInfo`."""
        return await self._client.get("/api/system/info", model=SystemInfo)

    async def me(self) -> Me:
        """Fetch `/api/me` and return the typed authenticated user profile."""
        return await self._client.get("/api/me", model=Me)
