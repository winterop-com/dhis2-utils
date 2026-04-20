"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import TrackerStatus

if TYPE_CHECKING:
    from .persistence_report import PersistenceReport
    from .tracker_stats import TrackerStats
    from .validation_report import ValidationReport


class TrackerImportReport(_BaseModel):
    """OpenAPI schema `TrackerImportReport`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    bundleReport: PersistenceReport | None = None
    message: str | None = None
    stats: TrackerStats | None = None
    status: TrackerStatus | None = None
    validationReport: ValidationReport | None = None
