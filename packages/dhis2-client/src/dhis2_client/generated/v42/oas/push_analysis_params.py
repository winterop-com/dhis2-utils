"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .sharing import Sharing
    from .translation import Translation


class PushAnalysisParamsCreatedBy(_BaseModel):
    """OpenAPI schema `PushAnalysisParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class PushAnalysisParamsDashboard(_BaseModel):
    """OpenAPI schema `PushAnalysisParamsDashboard`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class PushAnalysisParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `PushAnalysisParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class PushAnalysisParamsRecipientUserGroups(_BaseModel):
    """OpenAPI schema `PushAnalysisParamsRecipientUserGroups`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class PushAnalysisParams(_BaseModel):
    """OpenAPI schema `PushAnalysisParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: PushAnalysisParamsCreatedBy | None = None
    dashboard: PushAnalysisParamsDashboard | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: PushAnalysisParamsLastUpdatedBy | None = None
    message: str | None = None
    name: str | None = None
    recipientUserGroups: list[PushAnalysisParamsRecipientUserGroups] | None = None
    sharing: Sharing | None = None
    title: str | None = None
    translations: list[Translation] | None = None
