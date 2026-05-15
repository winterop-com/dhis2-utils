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
    from .dimension_item_keywords import DimensionItemKeywords
    from .event_repetition import EventRepetition
    from .sharing import Sharing
    from .translation import Translation


class OptionGroupSetCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OptionGroupSetItems(_BaseModel):
    """A UID reference to a DimensionalItemObject  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OptionGroupSetLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OptionGroupSetLegendSet(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OptionGroupSetOptionGroups(_BaseModel):
    """A UID reference to a OptionGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OptionGroupSetOptionSet(_BaseModel):
    """A UID reference to a OptionSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OptionGroupSetProgram(_BaseModel):
    """A UID reference to a Program  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OptionGroupSetProgramStage(_BaseModel):
    """A UID reference to a ProgramStage  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OptionGroupSetUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OptionGroupSet(_BaseModel):
    """OpenAPI schema `OptionGroupSet`."""

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
    allItems: bool | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: OptionGroupSetCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    dataDimension: bool | None = None
    dataDimensionType: Literal["DISAGGREGATION", "ATTRIBUTE"] | None = None
    description: str | None = None
    dimension: str | None = None
    dimensionItemKeywords: DimensionItemKeywords | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    filter: str | None = None
    formName: str | None = None
    href: str | None = None
    id: str | None = None
    items: list[OptionGroupSetItems] | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: OptionGroupSetLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    legendSet: OptionGroupSetLegendSet | None = _Field(default=None, description="A UID reference to a LegendSet  ")
    name: str | None = None
    optionGroups: list[OptionGroupSetOptionGroups] | None = None
    optionSet: OptionGroupSetOptionSet | None = _Field(default=None, description="A UID reference to a OptionSet  ")
    program: OptionGroupSetProgram | None = _Field(default=None, description="A UID reference to a Program  ")
    programStage: OptionGroupSetProgramStage | None = _Field(
        default=None, description="A UID reference to a ProgramStage  "
    )
    repetition: EventRepetition | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    translations: list[Translation] | None = None
    user: OptionGroupSetUser | None = _Field(default=None, description="A UID reference to a User  ")
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
