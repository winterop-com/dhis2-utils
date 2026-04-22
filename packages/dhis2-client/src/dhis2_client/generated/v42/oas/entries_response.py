"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class EntriesResponsePager(_BaseModel):
    """OpenAPI schema `EntriesResponsePager`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    page: int | None = None
    pageSize: int | None = None


class EntriesResponse(_BaseModel):
    """OpenAPI schema `EntriesResponse`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    entries: list[dict[str, Any]] | None = None
    pager: EntriesResponsePager | None = None
