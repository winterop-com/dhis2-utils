"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import ImportStatus

if TYPE_CHECKING:
    from .import_options import ImportOptions
    from .import_summary import ImportSummary


class ImportSummaries(_BaseModel):
    """OpenAPI schema `ImportSummaries`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    deleted: int | None = None
    ignored: int | None = None
    importOptions: ImportOptions | None = None
    importSummaries: list[ImportSummary] | None = None
    imported: int | None = None
    responseType: str | None = None
    status: ImportStatus | None = None
    total: int | None = None
    updated: int | None = None
