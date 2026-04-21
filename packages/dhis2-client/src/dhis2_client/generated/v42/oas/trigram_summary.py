"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class TrigramSummary(_BaseModel):
    """OpenAPI schema `TrigramSummary`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    indexableAttributes: list[dict[str, Any]] | None = None
    indexedAttributes: list[dict[str, Any]] | None = None
    obsoleteIndexedAttributes: list[dict[str, Any]] | None = None
