"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class SharingUserAccess(_BaseModel):
    """OpenAPI schema `SharingUserAccess`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: str | None = None
    displayName: str | None = None
    id: str | None = None
    name: str | None = None
    username: str | None = None
