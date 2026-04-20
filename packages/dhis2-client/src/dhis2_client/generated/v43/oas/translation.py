"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class Translation(_BaseModel):
    """OpenAPI schema `Translation`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    locale: str | None = None
    property: str | None = None
    value: str | None = None
