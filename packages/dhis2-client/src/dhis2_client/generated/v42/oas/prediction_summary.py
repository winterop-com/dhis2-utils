"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import PredictionStatus


class PredictionSummary(_BaseModel):
    """OpenAPI schema `PredictionSummary`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    deleted: int
    description: str | None = None
    inserted: int
    predictors: int
    responseType: str | None = None
    status: PredictionStatus
    unchanged: int
    updated: int
