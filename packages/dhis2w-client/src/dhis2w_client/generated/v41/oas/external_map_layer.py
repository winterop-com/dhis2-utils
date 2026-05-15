"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .sharing import Sharing
    from .translation import Translation


class ExternalMapLayerCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ExternalMapLayerLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ExternalMapLayerLegendSet(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ExternalMapLayerUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ExternalMapLayer(_BaseModel):
    """OpenAPI schema `ExternalMapLayer`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    attribution: str | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ExternalMapLayerCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    imageFormat: Literal["PNG", "JPG"] | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ExternalMapLayerLastUpdatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    layers: str | None = None
    legendSet: ExternalMapLayerLegendSet | None = _Field(default=None, description="A UID reference to a LegendSet  ")
    legendSetUrl: str | None = None
    mapLayerPosition: Literal["BASEMAP", "OVERLAY"] | None = None
    mapService: Literal["WMS", "TMS", "XYZ", "VECTOR_STYLE", "GEOJSON_URL", "ARCGIS_FEATURE"] | None = None
    name: str | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
    url: str | None = None
    user: ExternalMapLayerUser | None = _Field(default=None, description="A UID reference to a User  ")
