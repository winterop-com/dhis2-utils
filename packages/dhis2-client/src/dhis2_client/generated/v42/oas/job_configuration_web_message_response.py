"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import JobStatus, JobType


class JobConfigurationWebMessageResponse(_BaseModel):
    """OpenAPI schema `JobConfigurationWebMessageResponse`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    created: datetime | None = None
    id: str | None = None
    jobParameters: dict[str, Any] | None = None
    jobStatus: JobStatus | None = None
    jobType: JobType | None = None
    name: str | None = None
    relativeNotifierEndpoint: str | None = None
    responseType: str | None = None
