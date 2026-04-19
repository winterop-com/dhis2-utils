"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import ImportStatus

if TYPE_CHECKING:
    from .import_options import ImportOptions
    from .import_summary import ImportSummary


class ImportSummaries(_BaseModel):
    """OpenAPI schema `ImportSummaries`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    deleted: int
    ignored: int
    importOptions: ImportOptions | None = None
    importSummaries: list[ImportSummary] | None = None
    imported: int
    responseType: str | None = None
    status: ImportStatus
    total: int
    updated: int
