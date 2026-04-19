"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class AddIconRequest(_BaseModel):
    """OpenAPI schema `AddIconRequest`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    description: str | None = None
    fileResourceId: str | None = None
    key: str | None = None
    keywords: list[str] | None = None
