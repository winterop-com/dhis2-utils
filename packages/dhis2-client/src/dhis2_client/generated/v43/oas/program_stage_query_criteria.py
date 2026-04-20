"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AssignedUserSelectionMode, EnrollmentStatus, EventStatus, OrganisationUnitSelectionMode

if TYPE_CHECKING:
    from .attribute_value_filter import AttributeValueFilter
    from .date_filter_period import DateFilterPeriod
    from .event_data_filter import EventDataFilter


class ProgramStageQueryCriteria(_BaseModel):
    """OpenAPI schema `ProgramStageQueryCriteria`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    assignedUserMode: AssignedUserSelectionMode | None = None
    assignedUsers: list[str] | None = None
    attributeValueFilters: list[AttributeValueFilter] | None = None
    dataFilters: list[EventDataFilter] | None = None
    displayColumnOrder: list[str] | None = None
    enrolledAt: DateFilterPeriod | None = None
    enrollmentOccurredAt: DateFilterPeriod | None = None
    enrollmentStatus: EnrollmentStatus | None = None
    eventCreatedAt: DateFilterPeriod | None = None
    eventOccurredAt: DateFilterPeriod | None = None
    eventScheduledAt: DateFilterPeriod | None = None
    eventStatus: EventStatus | None = None
    followUp: bool | None = None
    order: str | None = None
    orgUnit: str | None = None
    ouMode: OrganisationUnitSelectionMode | None = None
