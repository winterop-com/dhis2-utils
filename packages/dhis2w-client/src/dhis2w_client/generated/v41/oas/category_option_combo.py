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
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class CategoryOptionComboCategoryCombo(_BaseModel):
    """A UID reference to a CategoryCombo  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionComboCategoryOptions(_BaseModel):
    """A UID reference to a CategoryOption  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionComboCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionComboLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionComboLegendSet(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionComboLegendSets(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionComboUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionCombo(_BaseModel):
    """OpenAPI schema `CategoryOptionCombo`."""

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
    categoryCombo: CategoryOptionComboCategoryCombo | None = _Field(
        default=None, description="A UID reference to a CategoryCombo  "
    )
    categoryOptions: list[CategoryOptionComboCategoryOptions] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: CategoryOptionComboCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    description: str | None = None
    dimensionItem: str | None = None
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
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    href: str | None = None
    id: str | None = None
    ignoreApproval: bool | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: CategoryOptionComboLastUpdatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    legendSet: CategoryOptionComboLegendSet | None = _Field(
        default=None, description="A UID reference to a LegendSet  "
    )
    legendSets: list[CategoryOptionComboLegendSets] | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
    user: CategoryOptionComboUser | None = _Field(default=None, description="A UID reference to a User  ")
