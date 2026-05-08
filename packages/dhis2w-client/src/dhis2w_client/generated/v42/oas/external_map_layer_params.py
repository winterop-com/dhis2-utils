"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import ImageFormat, MapLayerPosition, MapService

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .sharing import Sharing
    from .translation import Translation


class ExternalMapLayerParamsCreatedBy(_BaseModel):
    """OpenAPI schema `ExternalMapLayerParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ExternalMapLayerParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `ExternalMapLayerParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ExternalMapLayerParamsLegendSet(_BaseModel):
    """OpenAPI schema `ExternalMapLayerParamsLegendSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ExternalMapLayerParams(_BaseModel):
    """OpenAPI schema `ExternalMapLayerParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    attribution: str | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ExternalMapLayerParamsCreatedBy | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    imageFormat: ImageFormat | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ExternalMapLayerParamsLastUpdatedBy | None = None
    layers: str | None = None
    legendSet: ExternalMapLayerParamsLegendSet | None = None
    legendSetUrl: str | None = None
    mapLayerPosition: MapLayerPosition | None = None
    mapService: MapService | None = None
    name: str | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
    url: str | None = None
