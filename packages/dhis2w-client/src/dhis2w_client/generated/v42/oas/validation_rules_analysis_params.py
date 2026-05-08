"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class ValidationRulesAnalysisParams(_BaseModel):
    """OpenAPI schema `ValidationRulesAnalysisParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    endDate: str | None = None
    maxResults: int | None = None
    notification: bool | None = None
    ou: str | None = None
    persist: bool | None = None
    startDate: str | None = None
    vrg: str | None = None
