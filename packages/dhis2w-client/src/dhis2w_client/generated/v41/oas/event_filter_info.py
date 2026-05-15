"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .filter_period import FilterPeriod


class EventFilterInfo(_BaseModel):
    """OpenAPI schema `EventFilterInfo`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    assignedUserMode: Literal["CURRENT", "PROVIDED", "NONE", "ANY", "ALL"] | None = None
    assignedUsers: list[str] | None = None
    eventCreatedPeriod: FilterPeriod | None = None
    eventStatus: Literal["ACTIVE", "COMPLETED", "VISITED", "SCHEDULE", "OVERDUE", "SKIPPED"] | None = None
    programStage: str | None = None
