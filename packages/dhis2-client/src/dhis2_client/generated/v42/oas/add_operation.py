"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class AddOperation(_BaseModel):
    """OpenAPI schema `AddOperation`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    op: str | None = None
    path: str | None = None
    value: Any | None = None
