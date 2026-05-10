"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class Config(_BaseModel):
    """OpenAPI schema `Config`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    inclusionStrategy: str | None = None
    properties: dict[str, dict[str, Any]] | None = None
