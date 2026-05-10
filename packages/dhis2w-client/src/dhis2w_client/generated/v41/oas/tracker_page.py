"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .tracker_pager import TrackerPager


class TrackerPage(_BaseModel):
    """OpenAPI schema `TrackerPage`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    page: int | None = None
    pageCount: int | None = None
    pageSize: int | None = None
    pager: TrackerPager | None = None
    total: int | None = None
