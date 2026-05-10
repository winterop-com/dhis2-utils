"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class MetadataAdjustParams(_BaseModel):
    """OpenAPI schema `MetadataAdjustParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    change: dict[str, Any] | None = None
    targetId: str | None = None
