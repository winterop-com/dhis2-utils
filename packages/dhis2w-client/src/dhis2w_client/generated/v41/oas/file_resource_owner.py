"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class FileResourceOwner(_BaseModel):
    """OpenAPI schema `FileResourceOwner`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    co: str | None = None
    de: str | None = None
    domain: str | None = None
    id: str | None = None
    ou: str | None = None
    pe: str | None = None
