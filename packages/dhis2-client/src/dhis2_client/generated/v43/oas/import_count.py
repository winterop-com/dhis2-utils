"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class ImportCount(_BaseModel):
    """OpenAPI schema `ImportCount`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    deleted: int | None = None
    ignored: int | None = None
    imported: int | None = None
    updated: int | None = None
