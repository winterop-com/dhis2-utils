"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .date_filter_period import DateFilterPeriod
    from .event_data_filter import EventDataFilter


class EventQueryCriteria(_BaseModel):
    """OpenAPI schema `EventQueryCriteria`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    assignedUserMode: str | None = None
    assignedUsers: list[str] | None = None
    completedDate: DateFilterPeriod | None = None
    dataFilters: list[EventDataFilter] | None = None
    displayColumnOrder: list[str] | None = None
    dueDate: DateFilterPeriod | None = None
    eventDate: DateFilterPeriod | None = None
    events: list[str] | None = None
    followUp: bool | None = None
    lastUpdatedDate: DateFilterPeriod | None = None
    order: str | None = None
    organisationUnit: str | None = None
    ouMode: str | None = None
    status: str | None = None
