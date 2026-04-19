"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AggregationType, DimensionItemType, DimensionType, TotalAggregationType, ValueType

if TYPE_CHECKING:
    from .object_style import ObjectStyle


class MetadataItemParamsIndicatorType(_BaseModel):
    """OpenAPI schema `MetadataItemParamsIndicatorType`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class MetadataItemParams(_BaseModel):
    """OpenAPI schema `MetadataItemParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aggregationType: AggregationType
    code: str | None = None
    description: str | None = None
    dimensionItemType: DimensionItemType
    dimensionType: DimensionType
    endDate: datetime | None = None
    expression: str | None = None
    indicatorType: MetadataItemParamsIndicatorType | None = None
    legendSet: str | None = None
    name: str | None = None
    options: list[dict[str, str]] | None = None
    startDate: datetime | None = None
    style: ObjectStyle | None = None
    totalAggregationType: TotalAggregationType
    uid: str | None = None
    valueType: ValueType
