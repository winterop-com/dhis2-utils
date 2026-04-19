"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._aliases import Instant
from ._enums import ValueType


class TrackerAttribute(_BaseModel):
    """OpenAPI schema `TrackerAttribute`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attribute: str | None = None
    code: str | None = None
    createdAt: Instant | None = None
    displayName: str | None = None
    storedBy: str | None = None
    updatedAt: Instant | None = None
    value: str | None = None
    valueType: ValueType | None = None
