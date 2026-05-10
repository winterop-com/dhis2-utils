"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class GeoFeature(_BaseModel):
    """OpenAPI schema `GeoFeature`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    co: str | None = None
    code: str | None = None
    dimensions: dict[str, str] | None = None
    hcd: bool | None = None
    hcu: bool | None = None
    id: str | None = None
    le: int | None = None
    na: str | None = None
    pg: str | None = None
    pi: str | None = None
    pn: str | None = None
    ty: int | None = None
