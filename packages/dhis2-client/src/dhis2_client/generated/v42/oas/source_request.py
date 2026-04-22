"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import AggregationType

if TYPE_CHECKING:
    from .filter import Filter


class SourceRequest(_BaseModel):
    """OpenAPI schema `SourceRequest`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aggregationType: AggregationType | None = None
    dx: list[str] | None = None
    filters: list[Filter] | None = None
    inputIdScheme: str | None = None
    name: str | None = None
    ou: list[str] | None = None
    outputDataElementIdScheme: str | None = None
    outputDataItemIdScheme: str | None = None
    outputIdScheme: str | None = None
    outputOrgUnitIdScheme: str | None = None
    pe: list[str] | None = None
    visualization: str | None = None
