"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .tracker_user import TrackerUser


class TrackerDataValue(_BaseModel):
    """OpenAPI schema `TrackerDataValue`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    createdAt: datetime | int | None = None
    createdBy: TrackerUser | None = None
    dataElement: str | None = _Field(default=None, description="A UID for an DataElement object  ")
    providedElsewhere: bool | None = None
    storedBy: str | None = None
    updatedAt: datetime | int | None = None
    updatedBy: TrackerUser | None = None
    value: str | None = None
