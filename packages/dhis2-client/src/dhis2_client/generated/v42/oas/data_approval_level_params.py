"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .category_option_group_set_params import CategoryOptionGroupSetParams
    from .sharing import Sharing
    from .translation import Translation


class DataApprovalLevelParamsCreatedBy(_BaseModel):
    """OpenAPI schema `DataApprovalLevelParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataApprovalLevelParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `DataApprovalLevelParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataApprovalLevelParams(_BaseModel):
    """OpenAPI schema `DataApprovalLevelParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    categoryOptionGroupSet: CategoryOptionGroupSetParams | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: DataApprovalLevelParamsCreatedBy | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: DataApprovalLevelParamsLastUpdatedBy | None = None
    level: int | None = None
    name: str | None = None
    orgUnitLevel: int | None = None
    orgUnitLevelName: str | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
