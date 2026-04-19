"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .keyword_params import KeywordParams


class DimensionItemKeywordsParams(_BaseModel):
    """OpenAPI schema `DimensionItemKeywordsParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    empty: bool | None = None
    keywords: list[KeywordParams] | None = None
