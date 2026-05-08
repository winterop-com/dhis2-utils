"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._aliases import Instant

if TYPE_CHECKING:
    from .tracker_user import TrackerUser


class TrackerDataValue(_BaseModel):
    """OpenAPI schema `TrackerDataValue`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    createdAt: Instant | None = None
    createdBy: TrackerUser | None = None
    dataElement: str | None = None
    providedElsewhere: bool | None = None
    storedBy: str | None = None
    updatedAt: Instant | None = None
    updatedBy: TrackerUser | None = None
    value: str | None = None
