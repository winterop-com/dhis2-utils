"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class DeprecatedTrackerAttribute(_BaseModel):
    """OpenAPI schema `Deprecated_TrackerAttribute`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attribute: str | None = None
    code: str | None = None
    created: str | None = None
    displayName: str | None = None
    lastUpdated: str | None = None
    storedBy: str | None = None
    value: str | None = None
    valueType: str | None = None
