"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._aliases import Instant

if TYPE_CHECKING:
    from .tracker_user import TrackerUser


class TrackerNote(_BaseModel):
    """OpenAPI schema `TrackerNote`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    createdBy: TrackerUser | None = None
    note: str | None = None
    storedAt: Instant | None = None
    storedBy: str | None = None
    value: str | None = None
