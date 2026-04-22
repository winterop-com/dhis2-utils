"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .data_integrity_issue import DataIntegrityIssue


class DataIntegrityDetails(_BaseModel):
    """OpenAPI schema `DataIntegrityDetails`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    error: str | None = None
    finishedTime: datetime | None = None
    issues: list[DataIntegrityIssue] | None = None
    startTime: datetime | None = None
