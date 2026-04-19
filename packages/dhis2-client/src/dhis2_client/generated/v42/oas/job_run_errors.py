"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import JobType

if TYPE_CHECKING:
    from .job_run_error import JobRunError


class JobRunErrors(_BaseModel):
    """OpenAPI schema `JobRunErrors`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    codes: str | None = None
    created: datetime | None = None
    errors: list[JobRunError] | None = None
    executed: datetime | None = None
    file: str | None = _Field(default=None, description="The file resource used to store the job\u0027s input")
    filesize: int | None = None
    filetype: str | None = None
    finished: datetime | None = None
    id: str | None = None
    type: JobType | None = None
    user: str | None = None
