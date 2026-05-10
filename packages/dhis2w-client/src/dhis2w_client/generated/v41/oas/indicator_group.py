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


class IndicatorGroupCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IndicatorGroupGroupSets(_BaseModel):
    """A UID reference to a IndicatorGroupSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IndicatorGroupIndicatorGroupSet(_BaseModel):
    """A UID reference to a IndicatorGroupSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IndicatorGroupIndicators(_BaseModel):
    """A UID reference to a Indicator  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IndicatorGroupLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IndicatorGroupUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IndicatorGroup(_BaseModel):
    """OpenAPI schema `IndicatorGroup`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: IndicatorGroupCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    description: str | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    groupSets: list[IndicatorGroupGroupSets] | None = None
    href: str | None = None
    id: str | None = None
    indicatorGroupSet: IndicatorGroupIndicatorGroupSet | None = _Field(
        default=None, description="A UID reference to a IndicatorGroupSet  "
    )
    indicators: list[IndicatorGroupIndicators] | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: IndicatorGroupLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    name: str | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
    user: IndicatorGroupUser | None = _Field(default=None, description="A UID reference to a User  ")
