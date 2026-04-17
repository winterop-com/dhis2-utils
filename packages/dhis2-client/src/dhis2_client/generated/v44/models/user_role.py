"""Generated UserRole model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class UserRole(BaseModel):
    """DHIS2 UserRole resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    attributeValues: Any | None = None

    authorities: list[Any] | None = None

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    description: str | None = None

    displayName: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = None

    href: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    name: str | None = None

    restrictions: list[Any] | None = None

    sharing: Any | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    user: Reference | None = None

    users: list[Any] | None = None
