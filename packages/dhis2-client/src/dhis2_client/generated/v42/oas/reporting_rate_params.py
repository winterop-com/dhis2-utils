"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AggregationType, ReportingRateMetric

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .data_set_params import DataSetParams
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class ReportingRateParamsCreatedBy(_BaseModel):
    """OpenAPI schema `ReportingRateParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ReportingRateParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `ReportingRateParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ReportingRateParamsLegendSet(_BaseModel):
    """OpenAPI schema `ReportingRateParamsLegendSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ReportingRateParams(_BaseModel):
    """OpenAPI schema `ReportingRateParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aggregationType: AggregationType | None = None
    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ReportingRateParamsCreatedBy | None = None
    dataSet: DataSetParams | None = None
    description: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ReportingRateParamsLastUpdatedBy | None = None
    legendSet: ReportingRateParamsLegendSet | None = None
    metric: ReportingRateMetric | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
