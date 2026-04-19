"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AssignedUserSelectionMode, EventStatus

if TYPE_CHECKING:
    from .filter_period import FilterPeriod


class EventFilterInfo(_BaseModel):
    """OpenAPI schema `EventFilterInfo`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    assignedUserMode: AssignedUserSelectionMode
    assignedUsers: list[str] | None = None
    eventCreatedPeriod: FilterPeriod | None = None
    eventStatus: EventStatus
    programStage: str | None = None
