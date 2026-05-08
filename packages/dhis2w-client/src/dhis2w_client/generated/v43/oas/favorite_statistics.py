"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class FavoriteStatistics(_BaseModel):
    """OpenAPI schema `FavoriteStatistics`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    created: datetime | None = None
    id: str | None = None
    name: str | None = None
    position: int | None = None
    views: int | None = None
