"""Typed accessors for /api/system/info and /api/me (non-metadata system endpoints).

`SystemInfo` re-exports from `generated/v42/oas` — OpenAPI ships the full
shape (46 fields including `buildTime`, `databaseInfo`, analytics-table
timings, memory info). `Me` stays hand-written because `/api/me` isn't in
the OpenAPI spec under that name.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, ConfigDict, field_validator

from dhis2_client.generated.v42.oas import SystemInfo

if TYPE_CHECKING:
    from dhis2_client.client import Dhis2Client


class DisplayRef(BaseModel):
    """Minimal DHIS2 object reference carrying id + displayName for CLI rendering."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None
    displayName: str | None = None


def _coerce_refs(value: Any) -> Any:
    """Coerce a DHIS2 ref list to `list[DisplayRef]`, lifting bare-UID strings to `{id}` refs.

    `/api/me` returns `programs` as a flat list of UID strings in v42 even
    when `fields=programs[id,displayName]` is requested (see
    `user.service.current_user` for the server-side workaround). Accept both
    shapes here so direct `client.system.me()` calls don't blow up on the
    bare-string case.
    """
    if not isinstance(value, list):
        return value
    return [{"id": entry} if isinstance(entry, str) else entry for entry in value]


class Me(BaseModel):
    """Shape of `/api/me` for the authenticated user (common fields; unknown preserved).

    Hand-written: `/api/me` doesn't appear in the OpenAPI spec as a component
    schema, so the emitter can't generate it. This is a stable-enough subset
    of the real response — `extra="allow"` preserves anything else DHIS2 ships.
    """

    model_config = ConfigDict(extra="allow")

    id: str | None = None
    username: str | None = None
    displayName: str | None = None
    email: str | None = None
    firstName: str | None = None
    surname: str | None = None
    lastLogin: str | None = None
    created: str | None = None
    authorities: list[str] | None = None
    organisationUnits: list[DisplayRef] | None = None
    dataViewOrganisationUnits: list[DisplayRef] | None = None
    userGroups: list[DisplayRef] | None = None
    programs: list[DisplayRef] | None = None

    @field_validator(
        "organisationUnits",
        "dataViewOrganisationUnits",
        "userGroups",
        "programs",
        mode="before",
    )
    @classmethod
    def _coerce_ref_lists(cls, value: Any) -> Any:
        """Accept bare UID strings as well as `{id, displayName}` dicts on every ref-list field."""
        return _coerce_refs(value)


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


__all__ = ["DisplayRef", "Me", "SystemInfo", "SystemModule"]
