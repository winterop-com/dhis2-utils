"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class FontStyle(_BaseModel):
    """OpenAPI schema `FontStyle`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    bold: bool | None = None
    font: Literal["ARIAL", "SANS_SERIF", "VERDANA", "ROBOTO"] | None = None
    fontSize: int | None = None
    italic: bool | None = None
    textAlign: Literal["LEFT", "CENTER", "RIGHT"] | None = None
    textColor: str | None = None
    underline: bool | None = None
