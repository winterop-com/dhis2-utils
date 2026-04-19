"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import JobProgressStatus

if TYPE_CHECKING:
    from .stage import Stage


class Process(_BaseModel):
    """OpenAPI schema `Process`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    cancelledTime: datetime | None = None
    complete: bool | None = None
    completedTime: datetime | None = None
    description: str | None = None
    duration: int | None = None
    error: str | None = None
    jobId: str | None = None
    stages: list[Stage] | None = None
    status: JobProgressStatus | None = None
    summary: str | None = None
    userId: str | None = None
