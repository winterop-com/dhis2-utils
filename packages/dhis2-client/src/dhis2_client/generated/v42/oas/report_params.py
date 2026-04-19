"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import CacheStrategy, ReportType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .relative_periods import RelativePeriods
    from .reporting_params import ReportingParams
    from .sharing import Sharing
    from .translation import Translation
    from .visualization_params import VisualizationParams


class ReportParamsCreatedBy(_BaseModel):
    """OpenAPI schema `ReportParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class ReportParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `ReportParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class ReportParams(_BaseModel):
    """OpenAPI schema `ReportParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    cacheStrategy: CacheStrategy
    code: str | None = None
    created: datetime | None = None
    createdBy: ReportParamsCreatedBy | None = None
    designContent: str | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ReportParamsLastUpdatedBy | None = None
    name: str | None = None
    relativePeriods: RelativePeriods | None = None
    reportParams: ReportingParams | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
    type: ReportType
    visualization: VisualizationParams | None = None
