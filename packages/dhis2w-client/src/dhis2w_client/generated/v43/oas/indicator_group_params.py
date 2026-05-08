"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .indicator_group_set_params import IndicatorGroupSetParams
    from .sharing import Sharing
    from .translation import Translation


class IndicatorGroupParamsCreatedBy(_BaseModel):
    """OpenAPI schema `IndicatorGroupParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IndicatorGroupParamsGroupSets(_BaseModel):
    """OpenAPI schema `IndicatorGroupParamsGroupSets`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IndicatorGroupParamsIndicators(_BaseModel):
    """OpenAPI schema `IndicatorGroupParamsIndicators`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IndicatorGroupParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `IndicatorGroupParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IndicatorGroupParams(_BaseModel):
    """OpenAPI schema `IndicatorGroupParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: IndicatorGroupParamsCreatedBy | None = None
    description: str | None = None
    displayName: str | None = None
    groupSets: list[IndicatorGroupParamsGroupSets] | None = None
    href: str | None = None
    id: str | None = None
    indicatorGroupSet: IndicatorGroupSetParams | None = None
    indicators: list[IndicatorGroupParamsIndicators] | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: IndicatorGroupParamsLastUpdatedBy | None = None
    name: str | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
