"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class IdentifiableObjectsParamsAdditions(_BaseModel):
    """OpenAPI schema `IdentifiableObjectsParamsAdditions`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class IdentifiableObjectsParamsDeletions(_BaseModel):
    """OpenAPI schema `IdentifiableObjectsParamsDeletions`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class IdentifiableObjectsParamsIdentifiableObjects(_BaseModel):
    """OpenAPI schema `IdentifiableObjectsParamsIdentifiableObjects`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class IdentifiableObjectsParams(_BaseModel):
    """OpenAPI schema `IdentifiableObjectsParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    additions: list[IdentifiableObjectsParamsAdditions] | None = None
    deletions: list[IdentifiableObjectsParamsDeletions] | None = None
    identifiableObjects: list[IdentifiableObjectsParamsIdentifiableObjects] | None = None
