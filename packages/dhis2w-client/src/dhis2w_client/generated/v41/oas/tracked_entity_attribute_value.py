"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class TrackedEntityAttributeValueTrackedEntityAttribute(_BaseModel):
    """A UID reference to a TrackedEntityAttribute  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityAttributeValueTrackedEntityInstance(_BaseModel):
    """A UID reference to a TrackedEntity  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityAttributeValue(_BaseModel):
    """OpenAPI schema `TrackedEntityAttributeValue`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    created: datetime | None = None
    lastUpdated: datetime | None = None
    storedBy: str | None = None
    trackedEntityAttribute: TrackedEntityAttributeValueTrackedEntityAttribute | None = _Field(
        default=None, description="A UID reference to a TrackedEntityAttribute  "
    )
    trackedEntityInstance: TrackedEntityAttributeValueTrackedEntityInstance | None = _Field(
        default=None, description="A UID reference to a TrackedEntity  "
    )
    value: str | None = None
