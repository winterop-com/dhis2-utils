"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class Item(_BaseModel):
    """OpenAPI schema `Item`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    complete: bool | None = None
    completedTime: datetime | None = None
    description: str | None = None
    duration: int | None = None
    error: str | None = None
    onFailure: str | None = None
    status: str | None = None
    summary: str | None = None
