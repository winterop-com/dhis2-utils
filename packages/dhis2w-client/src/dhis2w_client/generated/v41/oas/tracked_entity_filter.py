"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .entity_query_criteria import EntityQueryCriteria
    from .event_filter_info import EventFilterInfo
    from .filter_period import FilterPeriod
    from .object_style import ObjectStyle
    from .sharing import Sharing
    from .translation import Translation


class TrackedEntityFilterCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityFilterLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityFilterProgram(_BaseModel):
    """A UID reference to a Program  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityFilterUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityFilter(_BaseModel):
    """OpenAPI schema `TrackedEntityFilter`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: TrackedEntityFilterCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    description: str | None = None
    displayDescription: str | None = None
    displayName: str | None = None
    enrollmentCreatedPeriod: FilterPeriod | None = None
    enrollmentStatus: Literal["ACTIVE", "COMPLETED", "CANCELLED"] | None = None
    entityQueryCriteria: EntityQueryCriteria | None = None
    eventFilters: list[EventFilterInfo] | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    followup: bool | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: TrackedEntityFilterLastUpdatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    name: str | None = None
    program: TrackedEntityFilterProgram | None = _Field(default=None, description="A UID reference to a Program  ")
    sharing: Sharing | None = None
    sortOrder: int | None = None
    style: ObjectStyle | None = None
    translations: list[Translation] | None = None
    user: TrackedEntityFilterUser | None = _Field(default=None, description="A UID reference to a User  ")
