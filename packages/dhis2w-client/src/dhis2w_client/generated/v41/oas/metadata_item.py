"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .object_style import ObjectStyle


class MetadataItemIndicatorType(_BaseModel):
    """A UID reference to a IndicatorType  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MetadataItem(_BaseModel):
    """OpenAPI schema `MetadataItem`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

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
    code: str | None = None
    description: str | None = None
    dimensionItemType: (
        Literal[
            "DATA_ELEMENT",
            "DATA_ELEMENT_OPERAND",
            "INDICATOR",
            "REPORTING_RATE",
            "PROGRAM_DATA_ELEMENT",
            "PROGRAM_ATTRIBUTE",
            "PROGRAM_INDICATOR",
            "PERIOD",
            "ORGANISATION_UNIT",
            "CATEGORY_OPTION",
            "OPTION_GROUP",
            "DATA_ELEMENT_GROUP",
            "ORGANISATION_UNIT_GROUP",
            "CATEGORY_OPTION_GROUP",
            "EXPRESSION_DIMENSION_ITEM",
            "SUBEXPRESSION_DIMENSION_ITEM",
        ]
        | None
    ) = None
    dimensionType: (
        Literal[
            "DATA_X",
            "PROGRAM_DATA_ELEMENT",
            "PROGRAM_ATTRIBUTE",
            "PROGRAM_INDICATOR",
            "DATA_COLLAPSED",
            "CATEGORY_OPTION_COMBO",
            "ATTRIBUTE_OPTION_COMBO",
            "PERIOD",
            "ORGANISATION_UNIT",
            "CATEGORY_OPTION_GROUP_SET",
            "DATA_ELEMENT_GROUP_SET",
            "ORGANISATION_UNIT_GROUP_SET",
            "ORGANISATION_UNIT_GROUP",
            "CATEGORY",
            "OPTION_GROUP_SET",
            "VALIDATION_RULE",
            "STATIC",
            "ORGANISATION_UNIT_LEVEL",
        ]
        | None
    ) = None
    endDate: datetime | None = None
    expression: str | None = None
    indicatorType: MetadataItemIndicatorType | None = _Field(
        default=None, description="A UID reference to a IndicatorType  "
    )
    legendSet: str | None = None
    name: str | None = None
    options: list[dict[str, str]] | None = None
    startDate: datetime | None = None
    style: ObjectStyle | None = None
    totalAggregationType: Literal["NONE", "SUM", "AVERAGE"] | None = None
    uid: str | None = None
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
