"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._aliases import Object

if TYPE_CHECKING:
    from .grid_header import GridHeader
    from .performance_metrics import PerformanceMetrics
    from .reference import Reference


class Grid(_BaseModel):
    """OpenAPI schema `Grid`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    headerWidth: int | None = None
    headers: list[GridHeader] | None = None
    height: int | None = None
    internalMetaData: dict[str, Object] | None = None
    lastDataRow: bool | None = None
    metaColumnIndexes: list[int] | None = None
    metaData: dict[str, Object] | None = None
    metadataHeaders: list[GridHeader] | None = None
    performanceMetrics: PerformanceMetrics | None = None
    refs: list[Reference] | None = None
    rowContext: dict[str, dict[str, Object]] | None = _Field(
        default=None, description="keys are class java.lang.Integer"
    )
    rows: list[list[Object]] | None = None
    subtitle: str | None = None
    table: str | None = None
    title: str | None = None
    visibleHeaders: list[GridHeader] | None = None
    visibleRows: list[list[Object]] | None = None
    visibleWidth: int | None = None
    width: int | None = None
