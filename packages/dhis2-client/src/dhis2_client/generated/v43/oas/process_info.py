"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import JobProgressStatus


class ProcessInfo(_BaseModel):
    """OpenAPI schema `ProcessInfo`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    cancelledTime: datetime | None = None
    completedTime: datetime | None = None
    description: str | None = None
    error: str | None = None
    jobId: str | None = None
    stages: list[str] | None = None
    startedTime: datetime | None = None
    status: JobProgressStatus | None = None
    summary: str | None = None
