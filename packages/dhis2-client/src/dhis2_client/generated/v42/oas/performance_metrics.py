"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .execution_plan import ExecutionPlan


class PerformanceMetrics(_BaseModel):
    """OpenAPI schema `PerformanceMetrics`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    executionPlans: list[ExecutionPlan] | None = None
    totalTimeInMillis: float
