"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class ImportCountWebMessageResponse(_BaseModel):
    """OpenAPI schema `ImportCountWebMessageResponse`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    created: int | None = None
    deleted: int | None = None
    responseType: str | None = None
    updated: int | None = None
