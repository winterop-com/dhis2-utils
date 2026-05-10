"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .deprecated__tracker_relationship_item import DeprecatedTrackerRelationshipItem


class DeprecatedTrackerRelationship(_BaseModel):
    """OpenAPI schema `Deprecated_TrackerRelationship`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    bidirectional: bool | None = None
    created: str | None = None
    from_: DeprecatedTrackerRelationshipItem | None = _Field(default=None, alias="from")
    lastUpdated: str | None = None
    relationship: str | None = None
    relationshipName: str | None = None
    relationshipType: str | None = None
    to: DeprecatedTrackerRelationshipItem | None = None
