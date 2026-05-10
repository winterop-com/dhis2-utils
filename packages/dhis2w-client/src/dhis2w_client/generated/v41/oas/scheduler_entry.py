"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .scheduler_entry_job import SchedulerEntryJob


class SchedulerEntry(_BaseModel):
    """OpenAPI schema `SchedulerEntry`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    configurable: bool | None = None
    cronExpression: str | None = None
    delay: int | None = None
    enabled: bool | None = None
    maxDelayedExecutionTime: datetime | None = None
    name: str | None = None
    nextExecutionTime: datetime | None = None
    secondsToMaxDelayedExecutionTime: int | None = None
    secondsToNextExecutionTime: int | None = None
    sequence: list[SchedulerEntryJob] | None = None
    status: str | None = None
    type: str | None = None
