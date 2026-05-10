"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class TrackerAttribute(_BaseModel):
    """OpenAPI schema `TrackerAttribute`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attribute: str | None = _Field(default=None, description="A UID for an TrackerAttribute object  ")
    code: str | None = None
    createdAt: datetime | int | None = None
    displayName: str | None = None
    storedBy: str | None = None
    updatedAt: datetime | int | None = None
    value: str | None = None
    valueType: str | None = None
