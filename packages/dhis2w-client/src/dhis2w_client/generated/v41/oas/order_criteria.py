"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class OrderCriteria(_BaseModel):
    """OpenAPI schema `OrderCriteria`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    direction: Literal["ASC", "DESC"] | None = None
    field: str | None = None
