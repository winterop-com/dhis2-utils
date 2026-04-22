"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .import_report import ImportReport
    from .import_types_summary import ImportTypesSummary
    from .metadata_version import MetadataVersion


class MetadataSyncSummary(_BaseModel):
    """OpenAPI schema `MetadataSyncSummary`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    importReport: ImportReport | None = None
    importSummary: ImportTypesSummary | None = None
    metadataVersion: MetadataVersion | None = None
    responseType: str | None = None
