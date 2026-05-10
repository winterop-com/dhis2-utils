"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .map_view import MapView
    from .sharing import Sharing
    from .translation import Translation


class MapCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MapInterpretations(_BaseModel):
    """A UID reference to a Interpretation  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MapLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MapUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class Map(_BaseModel):
    """OpenAPI schema `Map`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    basemap: str | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: MapCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    description: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    href: str | None = None
    id: str | None = None
    interpretations: list[MapInterpretations] | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: MapLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    latitude: float | None = None
    longitude: float | None = None
    mapViews: list[MapView] | None = None
    name: str | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    subscribed: bool | None = None
    subscribers: list[str] | None = None
    title: str | None = None
    translations: list[Translation] | None = None
    user: MapUser | None = _Field(default=None, description="A UID reference to a User  ")
    zoom: int | None = None
