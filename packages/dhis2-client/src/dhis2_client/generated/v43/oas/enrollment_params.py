"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import EnrollmentStatus

if TYPE_CHECKING:
    from .relationship_item_params import RelationshipItemParams
    from .user_info_snapshot import UserInfoSnapshot


class EnrollmentParamsAttributeOptionCombo(_BaseModel):
    """OpenAPI schema `EnrollmentParamsAttributeOptionCombo`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EnrollmentParamsEvents(_BaseModel):
    """OpenAPI schema `EnrollmentParamsEvents`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EnrollmentParamsNotes(_BaseModel):
    """OpenAPI schema `EnrollmentParamsNotes`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EnrollmentParamsOrganisationUnit(_BaseModel):
    """OpenAPI schema `EnrollmentParamsOrganisationUnit`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EnrollmentParamsProgram(_BaseModel):
    """OpenAPI schema `EnrollmentParamsProgram`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EnrollmentParamsTrackedEntity(_BaseModel):
    """OpenAPI schema `EnrollmentParamsTrackedEntity`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EnrollmentParams(_BaseModel):
    """OpenAPI schema `EnrollmentParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeOptionCombo: EnrollmentParamsAttributeOptionCombo | None = None
    completedBy: str | None = None
    completedDate: datetime | None = None
    createdAtClient: datetime | None = None
    createdByUserInfo: UserInfoSnapshot | None = None
    deleted: bool | None = None
    enrollmentDate: datetime | None = None
    events: list[EnrollmentParamsEvents] | None = None
    followup: bool | None = None
    geometry: dict[str, Any] | None = None
    lastUpdatedAtClient: datetime | None = None
    lastUpdatedByUserInfo: UserInfoSnapshot | None = None
    notes: list[EnrollmentParamsNotes] | None = None
    occurredDate: datetime | None = None
    organisationUnit: EnrollmentParamsOrganisationUnit | None = None
    program: EnrollmentParamsProgram | None = None
    relationshipItems: list[RelationshipItemParams] | None = None
    status: EnrollmentStatus | None = None
    storedBy: str | None = None
    trackedEntity: EnrollmentParamsTrackedEntity | None = None
