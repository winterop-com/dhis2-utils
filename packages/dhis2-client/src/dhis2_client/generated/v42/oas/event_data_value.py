"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .user_info_snapshot import UserInfoSnapshot


class EventDataValue(_BaseModel):
    """OpenAPI schema `EventDataValue`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    created: datetime | None = None
    createdByUserInfo: UserInfoSnapshot | None = None
    lastUpdated: datetime | None = None
    lastUpdatedByUserInfo: UserInfoSnapshot | None = None
    providedElsewhere: bool | None = None
    storedBy: str | None = None
    value: str | None = None
