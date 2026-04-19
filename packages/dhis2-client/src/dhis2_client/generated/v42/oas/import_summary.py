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
    from .import_options import ImportOptions


class ImportSummary(_BaseModel):
    """OpenAPI schema `ImportSummary`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    conflicts: list[ImportConflict] | None = None
    dataSetComplete: str | None = None
    description: str | None = None
    href: str | None = None
    importCount: ImportCount | None = None
    importOptions: ImportOptions | None = None
    reference: str | None = None
    rejectedIndexes: list[int] | None = None
    responseType: str | None = None
    status: ImportStatus
