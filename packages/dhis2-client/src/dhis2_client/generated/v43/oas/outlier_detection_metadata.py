"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import Order, OutlierDetectionAlgorithm


class OutlierDetectionMetadata(_BaseModel):
    """OpenAPI schema `OutlierDetectionMetadata`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    algorithm: OutlierDetectionAlgorithm | None = None
    count: int | None = None
    dataEndDate: datetime | None = None
    dataStartDate: datetime | None = None
    maxResults: int | None = None
    orderBy: Order | None = None
    threshold: float | None = None
