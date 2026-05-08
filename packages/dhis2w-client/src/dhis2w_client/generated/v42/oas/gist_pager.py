"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class GistPager(_BaseModel):
    """OpenAPI schema `GistPager`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    nextPage: str | None = None
    page: int | None = None
    pageCount: int | None = None
    pageSize: int | None = None
    prevPage: str | None = None
    total: int | None = None
