"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class IdentifiableObjectsAdditions(_BaseModel):
    """A UID reference to a any type of object  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IdentifiableObjectsDeletions(_BaseModel):
    """A UID reference to a any type of object  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IdentifiableObjectsIdentifiableObjects(_BaseModel):
    """A UID reference to a any type of object  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IdentifiableObjects(_BaseModel):
    """OpenAPI schema `IdentifiableObjects`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    additions: list[IdentifiableObjectsAdditions] | None = None
    deletions: list[IdentifiableObjectsDeletions] | None = None
    identifiableObjects: list[IdentifiableObjectsIdentifiableObjects] | None = None
