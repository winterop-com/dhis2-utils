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

    category: JobType | None = None
    completed: bool | None = None
    data: Any | None = None
    dataType: NotificationDataType | None = None
    id: str | None = None
    level: NotificationLevel | None = None
    message: str | None = None
    time: datetime | None = None
    uid: str | None = None
