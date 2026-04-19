"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .object_report import ObjectReport
    from .stats import Stats


class TypeReport(_BaseModel):
    """OpenAPI schema `TypeReport`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    klass: str | None = None
    objectReports: list[ObjectReport]
    stats: Stats | None = None
