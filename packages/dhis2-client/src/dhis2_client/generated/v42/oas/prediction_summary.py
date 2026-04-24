"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import PredictionStatus


class PredictionSummary(_BaseModel):
    """OpenAPI schema `PredictionSummary`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    deleted: int | None = None
    description: str | None = None
    inserted: int | None = None
    predictors: int | None = None
    responseType: str | None = None
    status: PredictionStatus | None = None
    unchanged: int | None = None
    updated: int | None = None
