"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .sharing import Sharing
    from .translation import Translation


class TrackedEntityTypeAttributeCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityTypeAttributeLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityTypeAttributeTrackedEntityAttribute(_BaseModel):
    """A UID reference to a TrackedEntityAttribute  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityTypeAttributeTrackedEntityType(_BaseModel):
    """A UID reference to a TrackedEntityType  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityTypeAttributeUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityTypeAttribute(_BaseModel):
    """OpenAPI schema `TrackedEntityTypeAttribute`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: TrackedEntityTypeAttributeCreatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    displayInList: bool | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: TrackedEntityTypeAttributeLastUpdatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    mandatory: bool | None = None
    searchable: bool | None = None
    sharing: Sharing | None = None
    trackedEntityAttribute: TrackedEntityTypeAttributeTrackedEntityAttribute | None = _Field(
        default=None, description="A UID reference to a TrackedEntityAttribute  "
    )
    trackedEntityType: TrackedEntityTypeAttributeTrackedEntityType | None = _Field(
        default=None, description="A UID reference to a TrackedEntityType  "
    )
    translations: list[Translation] | None = None
    user: TrackedEntityTypeAttributeUser | None = _Field(default=None, description="A UID reference to a User  ")
    valueType: (
        Literal[
            "TEXT",
            "LONG_TEXT",
            "MULTI_TEXT",
            "LETTER",
            "PHONE_NUMBER",
            "EMAIL",
            "BOOLEAN",
            "TRUE_ONLY",
            "DATE",
            "DATETIME",
            "TIME",
            "NUMBER",
            "UNIT_INTERVAL",
            "PERCENTAGE",
            "INTEGER",
            "INTEGER_POSITIVE",
            "INTEGER_NEGATIVE",
            "INTEGER_ZERO_OR_POSITIVE",
            "TRACKER_ASSOCIATE",
            "USERNAME",
            "COORDINATE",
            "ORGANISATION_UNIT",
            "REFERENCE",
            "AGE",
            "URL",
            "FILE_RESOURCE",
            "IMAGE",
            "GEOJSON",
        ]
        | None
    ) = None
