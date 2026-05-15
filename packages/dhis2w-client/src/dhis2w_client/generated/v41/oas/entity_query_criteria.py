"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .attribute_value_filter import AttributeValueFilter
    from .date_filter_period import DateFilterPeriod


class EntityQueryCriteria(_BaseModel):
    """OpenAPI schema `EntityQueryCriteria`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    assignedUserMode: Literal["CURRENT", "PROVIDED", "NONE", "ANY", "ALL"] | None = None
    assignedUsers: list[str] | None = None
    attributeValueFilters: list[AttributeValueFilter] | None = None
    displayColumnOrder: list[str] | None = None
    enrollmentCreatedDate: DateFilterPeriod | None = None
    enrollmentIncidentDate: DateFilterPeriod | None = None
    enrollmentStatus: Literal["ACTIVE", "COMPLETED", "CANCELLED"] | None = None
    eventDate: DateFilterPeriod | None = None
    eventStatus: Literal["ACTIVE", "COMPLETED", "VISITED", "SCHEDULE", "OVERDUE", "SKIPPED"] | None = None
    followUp: bool | None = None
    lastUpdatedDate: DateFilterPeriod | None = None
    order: str | None = None
    organisationUnit: str | None = None
    ouMode: Literal["SELECTED", "CHILDREN", "DESCENDANTS", "ACCESSIBLE", "CAPTURE", "ALL"] | None = None
    programStage: str | None = None
    trackedEntityInstances: list[str] | None = None
    trackedEntityType: str | None = None
