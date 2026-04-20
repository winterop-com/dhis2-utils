"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class TrackerTrigramIndexJobParameters(_BaseModel):
    """OpenAPI schema `TrackerTrigramIndexJobParameters`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    runAnalyze: bool | None = None
