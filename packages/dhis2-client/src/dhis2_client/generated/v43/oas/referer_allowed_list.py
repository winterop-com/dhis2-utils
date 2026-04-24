"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class RefererAllowedList(_BaseModel):
    """OpenAPI schema `RefererAllowedList`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    allowedReferrers: list[str] | None = None
    type: str | None = None
