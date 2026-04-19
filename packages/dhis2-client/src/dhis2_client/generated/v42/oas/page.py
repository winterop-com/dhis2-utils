"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._aliases import EntityType

if TYPE_CHECKING:
    from .tracker_pager import TrackerPager


class Page(_BaseModel):
    """OpenAPI schema `Page`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    items: list[EntityType] | None = None
    pager: TrackerPager | None = None
