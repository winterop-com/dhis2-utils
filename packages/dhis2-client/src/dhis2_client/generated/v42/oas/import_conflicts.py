"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .import_conflict import ImportConflict


class ImportConflicts(_BaseModel):
    """OpenAPI schema `ImportConflicts`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    conflictCount: int | None = None
    conflicts: list[ImportConflict] | None = None
    conflictsDescription: str | None = None
    totalConflictOccurrenceCount: int | None = None
