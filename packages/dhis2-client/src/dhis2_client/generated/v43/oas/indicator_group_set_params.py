"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .sharing import Sharing
    from .translation import Translation


class IndicatorGroupSetParamsCreatedBy(_BaseModel):
    """OpenAPI schema `IndicatorGroupSetParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IndicatorGroupSetParamsIndicatorGroups(_BaseModel):
    """OpenAPI schema `IndicatorGroupSetParamsIndicatorGroups`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IndicatorGroupSetParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `IndicatorGroupSetParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IndicatorGroupSetParams(_BaseModel):
    """OpenAPI schema `IndicatorGroupSetParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    code: str | None = None
    compulsory: bool | None = None
    created: datetime | None = None
    createdBy: IndicatorGroupSetParamsCreatedBy | None = None
    description: str | None = None
    displayDescription: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    href: str | None = None
    id: str | None = None
    indicatorGroups: list[IndicatorGroupSetParamsIndicatorGroups] | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: IndicatorGroupSetParamsLastUpdatedBy | None = None
    name: str | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    translations: list[Translation] | None = None
