"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AnalyticsTablePhase, AnalyticsTableType, ResourceTableType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .sharing import Sharing
    from .translation import Translation


class AnalyticsTableHookParamsCreatedBy(_BaseModel):
    """OpenAPI schema `AnalyticsTableHookParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class AnalyticsTableHookParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `AnalyticsTableHookParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class AnalyticsTableHookParams(_BaseModel):
    """OpenAPI schema `AnalyticsTableHookParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    analyticsTableType: AnalyticsTableType | None = None
    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: AnalyticsTableHookParamsCreatedBy | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: AnalyticsTableHookParamsLastUpdatedBy | None = None
    name: str | None = None
    phase: AnalyticsTablePhase | None = None
    resourceTableType: ResourceTableType | None = None
    sharing: Sharing | None = None
    sql: str | None = None
    translations: list[Translation] | None = None
