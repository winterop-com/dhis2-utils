"""Generated Map model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class Map(BaseModel):
    """DHIS2 Map resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    attributeValues: Any | None = None

    basemap: str | None = None

    basemaps: list[Any] | None = None

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    description: str | None = None

    displayDescription: str | None = None

    displayFormName: str | None = None

    displayName: str | None = None

    displayShortName: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = None

    formName: str | None = None

    href: str | None = None

    interpretations: list[Any] | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    latitude: float | None = None

    longitude: float | None = None

    mapViews: list[Any] | None = None

    name: str | None = None

    sharing: Any | None = None

    shortName: str | None = None

    subscribed: bool | None = None

    subscribers: list[Any] | None = None

    title: str | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    user: Reference | None = None

    zoom: int | None = None
