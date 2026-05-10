"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class QueryAlias(_BaseModel):
    """OpenAPI schema `QueryAlias`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    href: str | None = None
    id: str | None = None
    path: str | None = None
    target: str | None = None
