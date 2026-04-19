"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .tracked_entity_attribute_params import TrackedEntityAttributeParams
    from .tracked_entity_params import TrackedEntityParams


class TrackedEntityAttributeValueParams(_BaseModel):
    """OpenAPI schema `TrackedEntityAttributeValueParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    created: datetime | None = None
    lastUpdated: datetime | None = None
    storedBy: str | None = None
    trackedEntityAttribute: TrackedEntityAttributeParams | None = None
    trackedEntityInstance: TrackedEntityParams | None = None
    value: str | None = None
