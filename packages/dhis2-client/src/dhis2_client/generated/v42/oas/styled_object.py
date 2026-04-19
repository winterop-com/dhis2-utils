"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import TextMode

if TYPE_CHECKING:
    from .font_style import FontStyle


class StyledObject(_BaseModel):
    """OpenAPI schema `StyledObject`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    fontStyle: FontStyle | None = None
    text: str | None = None
    textMode: TextMode | None = None
