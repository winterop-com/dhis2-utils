"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import ImportStatus

if TYPE_CHECKING:
    from .import_conflict import ImportConflict
    from .import_count import ImportCount


class GeoJsonImportReport(_BaseModel):
    """OpenAPI schema `GeoJsonImportReport`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    conflicts: list[ImportConflict] | None = None
    importCount: ImportCount | None = None
    responseType: str | None = None
    status: ImportStatus
    totalConflictOccurrenceCount: int
