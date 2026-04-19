"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .error_report import ErrorReport


class ObjectReport(_BaseModel):
    """OpenAPI schema `ObjectReport`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    displayName: str | None = None
    errorReports: list[ErrorReport]
    index: int | None = None
    klass: str | None = None
    uid: str | None = None
