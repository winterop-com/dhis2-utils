"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class ReservedValue(_BaseModel):
    """OpenAPI schema `ReservedValue`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    created: datetime | None = None
    expiryDate: datetime | None = None
    key: str | None = None
    ownerObject: str | None = None
    ownerUid: str | None = None
    value: str | None = None
