"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class ExecutionPlan(_BaseModel):
    """OpenAPI schema `ExecutionPlan`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    executionTime: float | None = None
    plan: dict[str, Any] | None = None
    planningTime: float | None = None
    query: str | None = None
    timeInMillis: float | None = None
