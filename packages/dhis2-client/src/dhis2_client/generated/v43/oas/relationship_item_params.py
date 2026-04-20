"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class RelationshipItemParamsEnrollment(_BaseModel):
    """OpenAPI schema `RelationshipItemParamsEnrollment`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class RelationshipItemParamsRelationship(_BaseModel):
    """OpenAPI schema `RelationshipItemParamsRelationship`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class RelationshipItemParamsSingleEvent(_BaseModel):
    """OpenAPI schema `RelationshipItemParamsSingleEvent`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class RelationshipItemParamsTrackedEntity(_BaseModel):
    """OpenAPI schema `RelationshipItemParamsTrackedEntity`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class RelationshipItemParamsTrackerEvent(_BaseModel):
    """OpenAPI schema `RelationshipItemParamsTrackerEvent`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class RelationshipItemParams(_BaseModel):
    """OpenAPI schema `RelationshipItemParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    enrollment: RelationshipItemParamsEnrollment | None = None
    id: int | None = None
    relationship: RelationshipItemParamsRelationship | None = None
    singleEvent: RelationshipItemParamsSingleEvent | None = None
    trackedEntity: RelationshipItemParamsTrackedEntity | None = None
    trackerEvent: RelationshipItemParamsTrackerEvent | None = None
