"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .object_style import ObjectStyle


class MetadataItemIndicatorType(_BaseModel):
    """A UID reference to a IndicatorType  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MetadataItem(_BaseModel):
    """OpenAPI schema `MetadataItem`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aggregationType: str | None = None
    code: str | None = None
    description: str | None = None
    dimensionItemType: str | None = None
    dimensionType: str | None = None
    endDate: datetime | None = None
    expression: str | None = None
    indicatorType: MetadataItemIndicatorType | None = _Field(
        default=None, description="A UID reference to a IndicatorType  "
    )
    legendSet: str | None = None
    name: str | None = None
    options: list[dict[str, str]] | None = None
    startDate: datetime | None = None
    style: ObjectStyle | None = None
    totalAggregationType: str | None = None
    uid: str | None = None
    valueType: str | None = None
