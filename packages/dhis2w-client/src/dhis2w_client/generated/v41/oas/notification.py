"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class Notification(_BaseModel):
    """OpenAPI schema `Notification`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    category: str | None = None
    completed: bool | None = None
    data: Any | None = None
    dataType: Literal["PARAMETERS"] = "PARAMETERS"
    id: str | None = None
    level: str | None = None
    message: str | None = None
    time: datetime | None = None
    uid: str | None = None
