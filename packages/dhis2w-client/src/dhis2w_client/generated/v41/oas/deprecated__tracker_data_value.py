"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .user_info_snapshot import UserInfoSnapshot


class DeprecatedTrackerDataValue(_BaseModel):
    """OpenAPI schema `Deprecated_TrackerDataValue`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    created: str | None = None
    createdByUserInfo: UserInfoSnapshot | None = None
    dataElement: str | None = None
    lastUpdated: str | None = None
    lastUpdatedByUserInfo: UserInfoSnapshot | None = None
    providedElsewhere: bool | None = None
    storedBy: str | None = None
    value: str | None = None
