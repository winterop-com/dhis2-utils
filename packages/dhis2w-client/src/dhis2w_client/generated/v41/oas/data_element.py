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
    from .data_set_element import DataSetElement
    from .file_type_value_options import FileTypeValueOptions
    from .object_style import ObjectStyle
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class DataElementCategoryCombo(_BaseModel):
    """A UID reference to a CategoryCombo  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementCommentOptionSet(_BaseModel):
    """A UID reference to a OptionSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementDataElementGroups(_BaseModel):
    """A UID reference to a DataElementGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementLegendSet(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementLegendSets(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementOptionSet(_BaseModel):
    """A UID reference to a OptionSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElement(_BaseModel):
    """OpenAPI schema `DataElement`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    aggregationLevels: list[int] | None = None
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
    categoryCombo: DataElementCategoryCombo | None = _Field(
        default=None, description="A UID reference to a CategoryCombo  "
    )
    code: str | None = None
    commentOptionSet: DataElementCommentOptionSet | None = _Field(
        default=None, description="A UID reference to a OptionSet  "
    )
    created: datetime | None = None
    createdBy: DataElementCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    dataElementGroups: list[DataElementDataElementGroups] | None = None
    dataSetElements: list[DataSetElement] | None = None
    description: str | None = None
    dimensionItem: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    domainType: Literal["AGGREGATE", "TRACKER"] | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    fieldMask: str | None = None
    formName: str | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: DataElementLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    legendSet: DataElementLegendSet | None = _Field(default=None, description="A UID reference to a LegendSet  ")
    legendSets: list[DataElementLegendSets] | None = None
    name: str | None = None
    optionSet: DataElementOptionSet | None = _Field(default=None, description="A UID reference to a OptionSet  ")
    optionSetValue: bool | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    style: ObjectStyle | None = None
    translations: list[Translation] | None = None
    url: str | None = None
    user: DataElementUser | None = _Field(default=None, description="A UID reference to a User  ")
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
    valueTypeOptions: FileTypeValueOptions | None = None
    zeroIsSignificant: bool | None = None
