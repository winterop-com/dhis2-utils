"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class AvailabilityStatus(_BaseModel):
    """OpenAPI schema `AvailabilityStatus`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    available: bool | None = None
    message: str | None = None
    statusCode: int
    statusPhrase: str | None = None
