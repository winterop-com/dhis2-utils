"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class FieldPathTransformer(_BaseModel):
    """OpenAPI schema `FieldPathTransformer`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    name: str | None = None
    parameters: list[str] | None = None
