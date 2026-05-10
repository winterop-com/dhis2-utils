"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class SchedulerEntryJob(_BaseModel):
    """OpenAPI schema `SchedulerEntryJob`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    cronExpression: str | None = None
    delay: int | None = None
    id: str | None = _Field(default=None, description="A UID for an JobConfiguration object  ")
    name: str | None = None
    nextExecutionTime: datetime | None = None
    status: str | None = None
    type: str | None = None
