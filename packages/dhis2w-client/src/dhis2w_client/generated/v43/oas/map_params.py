"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .basemap import Basemap
    from .map_view_params import MapViewParams
    from .sharing import Sharing
    from .translation import Translation


class MapParamsCreatedBy(_BaseModel):
    """OpenAPI schema `MapParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MapParamsInterpretations(_BaseModel):
    """OpenAPI schema `MapParamsInterpretations`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MapParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `MapParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MapParams(_BaseModel):
    """OpenAPI schema `MapParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    basemap: str | None = None
    basemaps: list[Basemap] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: MapParamsCreatedBy | None = None
    description: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    id: str | None = None
    interpretations: list[MapParamsInterpretations] | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: MapParamsLastUpdatedBy | None = None
    latitude: float | None = None
    longitude: float | None = None
    mapViews: list[MapViewParams] | None = None
    name: str | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    subscribed: bool | None = None
    subscribers: list[str] | None = None
    title: str | None = None
    translations: list[Translation] | None = None
    zoom: int | None = None
