"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class IndexResource(_BaseModel):
    """OpenAPI schema `IndexResource`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    displayName: str | None = None
    href: str | None = None
    plural: str | None = None
    singular: str | None = None
