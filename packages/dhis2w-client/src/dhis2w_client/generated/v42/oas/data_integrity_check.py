"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import DataIntegritySeverity


class DataIntegrityCheck(_BaseModel):
    """OpenAPI schema `DataIntegrityCheck`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    averageExecutionTime: int | None = None
    code: str | None = None
    description: str | None = None
    displayName: str | None = None
    introduction: str | None = None
    isProgrammatic: bool | None = None
    isSlow: bool | None = None
    issuesIdType: str | None = None
    name: str | None = None
    recommendation: str | None = None
    section: str | None = None
    sectionOrder: int | None = None
    severity: DataIntegritySeverity | None = None
