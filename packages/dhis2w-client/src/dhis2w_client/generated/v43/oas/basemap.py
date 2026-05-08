"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class Basemap(_BaseModel):
    """OpenAPI schema `Basemap`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    hidden: bool | None = None
    id: str | None = None
    opacity: float | None = None
