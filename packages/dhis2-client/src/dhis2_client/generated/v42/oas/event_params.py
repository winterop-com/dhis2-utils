"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import EventStatus

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .category_option_combo_params import CategoryOptionComboParams
    from .enrollment_params import EnrollmentParams
    from .event_data_value import EventDataValue
    from .organisation_unit_params import OrganisationUnitParams
    from .program_stage_params import ProgramStageParams
    from .relationship_item_params import RelationshipItemParams
    from .sharing import Sharing
    from .translation import Translation
    from .user_info_snapshot import UserInfoSnapshot
    from .user_params import UserParams


class EventParamsCreatedBy(_BaseModel):
    """OpenAPI schema `EventParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `EventParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventParamsMessageConversations(_BaseModel):
    """OpenAPI schema `EventParamsMessageConversations`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventParamsNotes(_BaseModel):
    """OpenAPI schema `EventParamsNotes`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventParams(_BaseModel):
    """OpenAPI schema `EventParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    assignedUser: UserParams | None = None
    attributeOptionCombo: CategoryOptionComboParams | None = None
    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    completed: bool | None = None
    completedBy: str | None = None
    completedDate: datetime | None = None
    creatableInSearchScope: bool | None = None
    created: datetime | None = None
    createdAtClient: datetime | None = None
    createdBy: EventParamsCreatedBy | None = None
    createdByUserInfo: UserInfoSnapshot | None = None
    deleted: bool | None = None
    displayName: str | None = None
    enrollment: EnrollmentParams | None = None
    eventDataValues: list[EventDataValue] | None = None
    eventDate: datetime | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    geometry: dict[str, Any] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedAtClient: datetime | None = None
    lastUpdatedBy: EventParamsLastUpdatedBy | None = None
    lastUpdatedByUserInfo: UserInfoSnapshot | None = None
    messageConversations: list[EventParamsMessageConversations] | None = None
    name: str | None = None
    notes: list[EventParamsNotes] | None = None
    organisationUnit: OrganisationUnitParams | None = None
    programStage: ProgramStageParams | None = None
    relationshipItems: list[RelationshipItemParams] | None = None
    scheduledDate: datetime | None = None
    sharing: Sharing | None = None
    status: EventStatus | None = None
    storedBy: str | None = None
    translations: list[Translation] | None = None
