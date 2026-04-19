"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class Pager(_BaseModel):
    """OpenAPI schema `Pager`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    nextPage: str | None = None
    page: int
    pageCount: int
    pageSize: int
    prevPage: str | None = None
    total: int
