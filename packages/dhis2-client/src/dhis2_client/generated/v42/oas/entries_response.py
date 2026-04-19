"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class EntriesResponsePager(_BaseModel):
    """OpenAPI schema `EntriesResponsePager`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    page: int
    pageSize: int


class EntriesResponse(_BaseModel):
    """OpenAPI schema `EntriesResponse`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    entries: list[dict[str, Any]] | None = None
    pager: EntriesResponsePager | None = None
