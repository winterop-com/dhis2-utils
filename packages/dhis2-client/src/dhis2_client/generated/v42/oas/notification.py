"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import JobType, NotificationDataType, NotificationLevel


class Notification(_BaseModel):
    """OpenAPI schema `Notification`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    category: JobType
    completed: bool | None = None
    data: Any | None = None
    dataType: NotificationDataType
    id: str | None = None
    level: NotificationLevel
    message: str | None = None
    time: datetime
    uid: str | None = None
