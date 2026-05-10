"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .field_path_transformer import FieldPathTransformer
    from .property import Property


class FieldPath(_BaseModel):
    """OpenAPI schema `FieldPath`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    exclude: bool | None = None
    fullPath: str | None = None
    name: str | None = None
    path: list[str] | None = None
    preset: bool | None = None
    property: Property | None = None
    root: bool | None = None
    transformer: bool | None = None
    transformers: list[FieldPathTransformer] | None = None
