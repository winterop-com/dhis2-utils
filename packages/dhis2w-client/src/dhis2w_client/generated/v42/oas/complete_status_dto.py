"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class CompleteStatusDto(_BaseModel):
    """OpenAPI schema `CompleteStatusDto`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    complete: bool | None = None
    created: datetime | None = None
    createdBy: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: str | None = None
