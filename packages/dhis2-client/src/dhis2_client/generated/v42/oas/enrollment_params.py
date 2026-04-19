"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import EnrollmentStatus

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .organisation_unit_params import OrganisationUnitParams
    from .program_params import ProgramParams
    from .relationship_item_params import RelationshipItemParams
    from .sharing import Sharing
    from .tracked_entity_params import TrackedEntityParams
    from .translation import Translation
    from .user_info_snapshot import UserInfoSnapshot


class EnrollmentParamsCreatedBy(_BaseModel):
    """OpenAPI schema `EnrollmentParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EnrollmentParamsEvents(_BaseModel):
    """OpenAPI schema `EnrollmentParamsEvents`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EnrollmentParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `EnrollmentParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EnrollmentParamsMessageConversations(_BaseModel):
    """OpenAPI schema `EnrollmentParamsMessageConversations`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EnrollmentParamsTrackedEntityComments(_BaseModel):
    """OpenAPI schema `EnrollmentParamsTrackedEntityComments`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EnrollmentParams(_BaseModel):
    """OpenAPI schema `EnrollmentParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    completedBy: str | None = None
    completedDate: datetime | None = None
    created: datetime | None = None
    createdAtClient: datetime | None = None
    createdBy: EnrollmentParamsCreatedBy | None = None
    createdByUserInfo: UserInfoSnapshot | None = None
    deleted: bool | None = None
    displayName: str | None = None
    enrollmentDate: datetime | None = None
    events: list[EnrollmentParamsEvents] | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    followup: bool | None = None
    geometry: dict[str, Any] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedAtClient: datetime | None = None
    lastUpdatedBy: EnrollmentParamsLastUpdatedBy | None = None
    lastUpdatedByUserInfo: UserInfoSnapshot | None = None
    messageConversations: list[EnrollmentParamsMessageConversations] | None = None
    name: str | None = None
    occurredDate: datetime | None = None
    organisationUnit: OrganisationUnitParams | None = None
    program: ProgramParams | None = None
    relationshipItems: list[RelationshipItemParams] | None = None
    sharing: Sharing | None = None
    status: EnrollmentStatus | None = None
    storedBy: str | None = None
    trackedEntityComments: list[EnrollmentParamsTrackedEntityComments] | None = None
    trackedEntityInstance: TrackedEntityParams | None = None
    translations: list[Translation] | None = None
