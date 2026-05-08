"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .import_count import ImportCount
    from .import_type_summary import ImportTypeSummary


class ImportTypesSummary(_BaseModel):
    """OpenAPI schema `ImportTypesSummary`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    importCount: ImportCount | None = None
    importTypeSummaries: list[ImportTypeSummary] | None = None
