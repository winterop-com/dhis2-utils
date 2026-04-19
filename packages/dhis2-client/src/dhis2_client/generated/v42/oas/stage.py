"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import FailurePolicy, JobProgressStatus

if TYPE_CHECKING:
    from .item import Item


class Stage(_BaseModel):
    """OpenAPI schema `Stage`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    complete: bool | None = None
    completedTime: datetime | None = None
    description: str | None = None
    duration: int
    error: str | None = None
    items: list[Item] | None = None
    onFailure: FailurePolicy
    status: JobProgressStatus
    summary: str | None = None
    totalItems: int
