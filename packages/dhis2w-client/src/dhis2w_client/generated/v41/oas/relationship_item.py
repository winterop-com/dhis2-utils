"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class RelationshipItemEnrollment(_BaseModel):
    """A UID reference to a Enrollment  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class RelationshipItemEvent(_BaseModel):
    """A UID reference to a Event  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class RelationshipItemRelationship(_BaseModel):
    """A UID reference to a Relationship  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class RelationshipItemTrackedEntity(_BaseModel):
    """A UID reference to a TrackedEntity  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class RelationshipItem(_BaseModel):
    """OpenAPI schema `RelationshipItem`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    enrollment: RelationshipItemEnrollment | None = _Field(
        default=None, description="A UID reference to a Enrollment  "
    )
    event: RelationshipItemEvent | None = _Field(default=None, description="A UID reference to a Event  ")
    relationship: RelationshipItemRelationship | None = _Field(
        default=None, description="A UID reference to a Relationship  "
    )
    trackedEntity: RelationshipItemTrackedEntity | None = _Field(
        default=None, description="A UID reference to a TrackedEntity  "
    )
