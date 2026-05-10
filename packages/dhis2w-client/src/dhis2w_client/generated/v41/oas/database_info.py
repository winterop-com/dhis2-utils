"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class DatabaseInfo(_BaseModel):
    """OpenAPI schema `DatabaseInfo`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    databaseVersion: str | None = None
    name: str | None = None
    spatialSupport: bool | None = None
    time: datetime | None = None
    url: str | None = None
    user: str | None = None
