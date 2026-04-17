"""Generated Dashboard model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class Dashboard(BaseModel):
    """DHIS2 Dashboard resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    allowedFilters: list[Any] | None = None

    attributeValues: Any | None = None

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    description: str | None = None

    displayDescription: str | None = None

    displayName: str | None = None

    embedded: Any | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = None

    href: str | None = None

    itemConfig: Any | None = None

    itemCount: int | None = None

    items: list[Any] | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    layout: Any | None = None

    name: str | None = None

    restrictFilters: bool | None = None

    sharing: Any | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    user: Reference | None = None
