"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._aliases import Instant

if TYPE_CHECKING:
    from .tracker_relationship_item import TrackerRelationshipItem


class TrackerRelationship(_BaseModel):
    """OpenAPI schema `TrackerRelationship`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    bidirectional: bool | None = None
    createdAt: Instant | None = None
    createdAtClient: Instant | None = None
    from_: TrackerRelationshipItem | None = _Field(default=None, alias="from")
    relationship: str | None = None
    relationshipName: str | None = None
    relationshipType: str | None = None
    to: TrackerRelationshipItem | None = None
    updatedAt: Instant | None = None
