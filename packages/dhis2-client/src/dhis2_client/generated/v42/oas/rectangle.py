"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class Rectangle(_BaseModel):
    """OpenAPI schema `Rectangle`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    count: int
    extent: str | None = None
