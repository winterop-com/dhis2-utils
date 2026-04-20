"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import NormalizedOutlierMethod, OutlierMethod

if TYPE_CHECKING:
    from .outlier_line import OutlierLine


class OutlierAnalysis(_BaseModel):
    """OpenAPI schema `OutlierAnalysis`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    enabled: bool | None = None
    extremeLines: OutlierLine | None = None
    maxResults: int | None = None
    normalizationMethod: NormalizedOutlierMethod | None = None
    outlierMethod: OutlierMethod | None = None
    thresholdFactor: float | None = None
