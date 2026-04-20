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


class EntityQueryCriteria(_BaseModel):
    """OpenAPI schema `EntityQueryCriteria`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    assignedUserMode: AssignedUserSelectionMode | None = None
    assignedUsers: list[str] | None = None
    attributeValueFilters: list[AttributeValueFilter] | None = None
    displayColumnOrder: list[str] | None = None
    enrollmentCreatedDate: DateFilterPeriod | None = None
    enrollmentIncidentDate: DateFilterPeriod | None = None
    enrollmentStatus: EnrollmentStatus | None = None
    eventDate: DateFilterPeriod | None = None
    eventStatus: EventStatus | None = None
    followUp: bool | None = None
    lastUpdatedDate: DateFilterPeriod | None = None
    order: str | None = None
    organisationUnit: str | None = None
    ouMode: OrganisationUnitSelectionMode | None = None
    programStage: str | None = None
    trackedEntityInstances: list[str] | None = None
    trackedEntityType: str | None = None
