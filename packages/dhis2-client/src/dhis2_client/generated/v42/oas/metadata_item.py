"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AggregationType, DimensionItemType, DimensionType, TotalAggregationType, ValueType

if TYPE_CHECKING:
    from .indicator_type import IndicatorType
    from .object_style import ObjectStyle


class MetadataItem(_BaseModel):
    """OpenAPI schema `MetadataItem`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aggregationType: AggregationType | None = None
    code: str | None = None
    description: str | None = None
    dimensionItemType: DimensionItemType | None = None
    dimensionType: DimensionType | None = None
    endDate: datetime | None = None
    expression: str | None = None
    indicatorType: IndicatorType | None = None
    legendSet: str | None = None
    name: str | None = None
    options: list[dict[str, str]] | None = None
    startDate: datetime | None = None
    style: ObjectStyle | None = None
    totalAggregationType: TotalAggregationType | None = None
    uid: str | None = None
    valueType: ValueType | None = None
