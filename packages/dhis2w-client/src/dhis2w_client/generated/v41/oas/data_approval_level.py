"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .sharing import Sharing
    from .translation import Translation


class DataApprovalLevelCategoryOptionGroupSet(_BaseModel):
    """A UID reference to a CategoryOptionGroupSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataApprovalLevelCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataApprovalLevelLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataApprovalLevelUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataApprovalLevel(_BaseModel):
    """OpenAPI schema `DataApprovalLevel`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    categoryOptionGroupSet: DataApprovalLevelCategoryOptionGroupSet | None = _Field(
        default=None, description="A UID reference to a CategoryOptionGroupSet  "
    )
    code: str | None = None
    created: datetime | None = None
    createdBy: DataApprovalLevelCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: DataApprovalLevelLastUpdatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    level: int | None = None
    name: str | None = None
    orgUnitLevel: int | None = None
    orgUnitLevelName: str | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
    user: DataApprovalLevelUser | None = _Field(default=None, description="A UID reference to a User  ")
