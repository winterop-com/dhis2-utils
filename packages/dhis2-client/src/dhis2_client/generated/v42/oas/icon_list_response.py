"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .pager import Pager


class IconListResponse(_BaseModel):
    """OpenAPI schema `IconListResponse`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    icons: list[dict[str, Any]] | None = None
    pager: Pager | None = None
