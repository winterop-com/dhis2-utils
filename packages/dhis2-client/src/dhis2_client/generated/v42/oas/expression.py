"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import MissingValueStrategy

if TYPE_CHECKING:
    from .translation import Translation


class Expression(_BaseModel):
    """OpenAPI schema `Expression`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    description: str | None = None
    displayDescription: str | None = None
    expression: str | None = None
    missingValueStrategy: MissingValueStrategy
    slidingWindow: bool | None = None
    translations: list[Translation] | None = None
