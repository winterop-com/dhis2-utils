"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class OutlierDetectionMetadata(_BaseModel):
    """OpenAPI schema `OutlierDetectionMetadata`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    algorithm: Literal["Z_SCORE", "MIN_MAX", "MOD_Z_SCORE", "INVALID_NUMERIC"] | None = None
    count: int | None = None
    dataEndDate: datetime | None = None
    dataStartDate: datetime | None = None
    maxResults: int | None = None
    orderBy: Literal["MEAN_ABS_DEV", "Z_SCORE"] | None = None
    threshold: float | None = None
