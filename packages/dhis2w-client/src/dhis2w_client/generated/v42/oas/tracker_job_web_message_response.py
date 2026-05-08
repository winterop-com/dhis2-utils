"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class TrackerJobWebMessageResponse(_BaseModel):
    """OpenAPI schema `TrackerJobWebMessageResponse`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None
    location: str | None = None
    responseType: str | None = None
