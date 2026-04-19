"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import MergeType

if TYPE_CHECKING:
    from .error_message import ErrorMessage


class MergeReport(_BaseModel):
    """OpenAPI schema `MergeReport`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    mergeErrors: list[ErrorMessage] | None = None
    mergeType: MergeType | None = None
    message: str | None = None
    sourcesDeleted: list[str] | None = None
