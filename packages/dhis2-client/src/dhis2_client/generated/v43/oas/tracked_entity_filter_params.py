"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import EnrollmentStatus

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .entity_query_criteria import EntityQueryCriteria
    from .event_filter_info import EventFilterInfo
    from .filter_period import FilterPeriod
    from .object_style import ObjectStyle
    from .program_params import ProgramParams
    from .sharing import Sharing
    from .translation import Translation


class TrackedEntityFilterParamsCreatedBy(_BaseModel):
    """OpenAPI schema `TrackedEntityFilterParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityFilterParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `TrackedEntityFilterParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityFilterParams(_BaseModel):
    """OpenAPI schema `TrackedEntityFilterParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: TrackedEntityFilterParamsCreatedBy | None = None
    description: str | None = None
    displayDescription: str | None = None
    displayName: str | None = None
    enrollmentCreatedPeriod: FilterPeriod | None = None
    enrollmentStatus: EnrollmentStatus | None = None
    entityQueryCriteria: EntityQueryCriteria | None = None
    eventFilters: list[EventFilterInfo] | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    followup: bool | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: TrackedEntityFilterParamsLastUpdatedBy | None = None
    name: str | None = None
    program: ProgramParams | None = None
    sharing: Sharing | None = None
    sortOrder: int | None = None
    style: ObjectStyle | None = None
    translations: list[Translation] | None = None
