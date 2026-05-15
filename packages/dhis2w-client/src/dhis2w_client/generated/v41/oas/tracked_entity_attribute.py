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
    from .object_style import ObjectStyle
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class TrackedEntityAttributeCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityAttributeLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityAttributeLegendSet(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityAttributeLegendSets(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityAttributeOptionSet(_BaseModel):
    """A UID reference to a OptionSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityAttributeUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityAttribute(_BaseModel):
    """OpenAPI schema `TrackedEntityAttribute`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    aggregationType: (
        Literal[
            "SUM",
            "AVERAGE",
            "AVERAGE_SUM_ORG_UNIT",
            "LAST",
            "LAST_AVERAGE_ORG_UNIT",
            "LAST_LAST_ORG_UNIT",
            "LAST_IN_PERIOD",
            "LAST_IN_PERIOD_AVERAGE_ORG_UNIT",
            "FIRST",
            "FIRST_AVERAGE_ORG_UNIT",
            "FIRST_FIRST_ORG_UNIT",
            "COUNT",
            "STDDEV",
            "VARIANCE",
            "MIN",
            "MAX",
            "MIN_SUM_ORG_UNIT",
            "MAX_SUM_ORG_UNIT",
            "NONE",
            "CUSTOM",
            "DEFAULT",
        ]
        | None
    ) = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    confidential: bool | None = None
    created: datetime | None = None
    createdBy: TrackedEntityAttributeCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    description: str | None = None
    dimensionItem: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayInListNoProgram: bool | None = None
    displayName: str | None = None
    displayOnVisitSchedule: bool | None = None
    displayShortName: str | None = None
    expression: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    fieldMask: str | None = None
    formName: str | None = None
    generated: bool | None = None
    href: str | None = None
    id: str | None = None
    inherit: bool | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: TrackedEntityAttributeLastUpdatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    legendSet: TrackedEntityAttributeLegendSet | None = _Field(
        default=None, description="A UID reference to a LegendSet  "
    )
    legendSets: list[TrackedEntityAttributeLegendSets] | None = None
    name: str | None = None
    optionSet: TrackedEntityAttributeOptionSet | None = _Field(
        default=None, description="A UID reference to a OptionSet  "
    )
    optionSetValue: bool | None = None
    orgunitScope: bool | None = None
    pattern: str | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    skipSynchronization: bool | None = None
    sortOrderInListNoProgram: int | None = None
    sortOrderInVisitSchedule: int | None = None
    style: ObjectStyle | None = None
    translations: list[Translation] | None = None
    unique: bool | None = None
    user: TrackedEntityAttributeUser | None = _Field(default=None, description="A UID reference to a User  ")
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
