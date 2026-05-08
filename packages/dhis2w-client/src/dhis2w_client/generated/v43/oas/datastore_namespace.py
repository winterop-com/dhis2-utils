"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class DatastoreNamespace(_BaseModel):
    """OpenAPI schema `DatastoreNamespace`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    authorities: list[str] | None = None
    namespace: str | None = None
    readOnlyAuthorities: list[str] | None = None
