"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class JsonRoot(_BaseModel):
    """OpenAPI schema `JsonRoot`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    properties: dict[str, dict[str, Any]] | None = None
