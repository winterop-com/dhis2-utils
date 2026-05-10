"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .user_info_snapshot import UserInfoSnapshot


class DeprecatedTrackerNote(_BaseModel):
    """OpenAPI schema `Deprecated_TrackerNote`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    lastUpdated: datetime | None = None
    lastUpdatedBy: UserInfoSnapshot | None = None
    note: str | None = None
    storedBy: str | None = None
    storedDate: str | None = None
    value: str | None = None
