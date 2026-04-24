"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .data_export_value import DataExportValue
    from .data_value_changelog_entry import DataValueChangelogEntry


class DataValueContextDto(_BaseModel):
    """OpenAPI schema `DataValueContextDto`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    audits: list[DataValueChangelogEntry] | None = None
    history: list[DataExportValue] | None = None
