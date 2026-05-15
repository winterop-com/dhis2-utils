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
    from .expression import Expression
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class ValidationRuleCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ValidationRuleLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ValidationRuleLegendSet(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ValidationRuleLegendSets(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ValidationRuleNotificationTemplates(_BaseModel):
    """A UID reference to a ValidationNotificationTemplate  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ValidationRuleUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ValidationRuleValidationRuleGroups(_BaseModel):
    """A UID reference to a ValidationRuleGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ValidationRule(_BaseModel):
    """OpenAPI schema `ValidationRule`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    aggregateExportAttributeOptionCombo: str | None = None
    aggregateExportCategoryOptionCombo: str | None = None
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
    created: datetime | None = None
    createdBy: ValidationRuleCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
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
    displayInstruction: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    href: str | None = None
    id: str | None = None
    importance: Literal["HIGH", "MEDIUM", "LOW"] | None = None
    instruction: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ValidationRuleLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    leftSide: Expression | None = None
    legendSet: ValidationRuleLegendSet | None = _Field(default=None, description="A UID reference to a LegendSet  ")
    legendSets: list[ValidationRuleLegendSets] | None = None
    name: str | None = None
    notificationTemplates: list[ValidationRuleNotificationTemplates] | None = None
    operator: (
        Literal[
            "equal_to",
            "not_equal_to",
            "greater_than",
            "greater_than_or_equal_to",
            "less_than",
            "less_than_or_equal_to",
            "compulsory_pair",
            "exclusive_pair",
        ]
        | None
    ) = None
    organisationUnitLevels: list[int] | None = None
    periodType: (
        Literal[
            "BiMonthly",
            "BiWeekly",
            "Daily",
            "FinancialApril",
            "FinancialJuly",
            "FinancialNov",
            "FinancialOct",
            "Monthly",
            "Quarterly",
            "QuarterlyNov",
            "SixMonthlyApril",
            "SixMonthlyNov",
            "SixMonthly",
            "TwoYearly",
            "Weekly",
            "WeeklySaturday",
            "WeeklySunday",
            "WeeklyThursday",
            "WeeklyWednesday",
            "Yearly",
        ]
        | None
    ) = None
    queryMods: QueryModifiers | None = None
    rightSide: Expression | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    skipFormValidation: bool | None = None
    translations: list[Translation] | None = None
    user: ValidationRuleUser | None = _Field(default=None, description="A UID reference to a User  ")
    validationRuleGroups: list[ValidationRuleValidationRuleGroups] | None = None
