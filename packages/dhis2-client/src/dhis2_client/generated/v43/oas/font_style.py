"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import Font, TextAlign


class FontStyle(_BaseModel):
    """OpenAPI schema `FontStyle`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    bold: bool | None = None
    font: Font | None = None
    fontSize: int | None = None
    italic: bool | None = None
    textAlign: TextAlign | None = None
    textColor: str | None = None
    underline: bool | None = None
