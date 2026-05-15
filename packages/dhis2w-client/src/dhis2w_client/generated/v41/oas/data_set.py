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
    from .data_element_operand import DataElementOperand
    from .data_input_period import DataInputPeriod
    from .data_set_element import DataSetElement
    from .object_style import ObjectStyle
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class DataSetCategoryCombo(_BaseModel):
    """A UID reference to a CategoryCombo  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataSetCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataSetDataEntryForm(_BaseModel):
    """A UID reference to a DataEntryForm  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataSetIndicators(_BaseModel):
    """A UID reference to a Indicator  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataSetInterpretations(_BaseModel):
    """A UID reference to a Interpretation  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataSetLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataSetLegendSet(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataSetLegendSets(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataSetNotificationRecipients(_BaseModel):
    """A UID reference to a UserGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataSetOrganisationUnits(_BaseModel):
    """A UID reference to a OrganisationUnit  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataSetSections(_BaseModel):
    """A UID reference to a Section  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataSetUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataSetWorkflow(_BaseModel):
    """A UID reference to a DataApprovalWorkflow  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataSet(_BaseModel):
    """OpenAPI schema `DataSet`."""

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
    categoryCombo: DataSetCategoryCombo | None = _Field(
        default=None, description="A UID reference to a CategoryCombo  "
    )
    code: str | None = None
    compulsoryDataElementOperands: list[DataElementOperand] | None = None
    compulsoryFieldsCompleteOnly: bool | None = None
    created: datetime | None = None
    createdBy: DataSetCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    dataElementDecoration: bool | None = None
    dataEntryForm: DataSetDataEntryForm | None = _Field(
        default=None, description="A UID reference to a DataEntryForm  "
    )
    dataInputPeriods: list[DataInputPeriod] | None = None
    dataSetElements: list[DataSetElement] | None = None
    description: str | None = None
    dimensionItem: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    expiryDays: int | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    fieldCombinationRequired: bool | None = None
    formName: str | None = None
    formType: Literal["DEFAULT", "CUSTOM", "SECTION", "SECTION_MULTIORG"] | None = None
    href: str | None = None
    id: str | None = None
    indicators: list[DataSetIndicators] | None = None
    interpretations: list[DataSetInterpretations] | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: DataSetLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    legendSet: DataSetLegendSet | None = _Field(default=None, description="A UID reference to a LegendSet  ")
    legendSets: list[DataSetLegendSets] | None = None
    mobile: bool | None = None
    name: str | None = None
    noValueRequiresComment: bool | None = None
    notificationRecipients: DataSetNotificationRecipients | None = _Field(
        default=None, description="A UID reference to a UserGroup  "
    )
    notifyCompletingUser: bool | None = None
    openFuturePeriods: int | None = None
    openPeriodsAfterCoEndDate: int | None = None
    organisationUnits: list[DataSetOrganisationUnits] | None = None
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
    renderAsTabs: bool | None = None
    renderHorizontally: bool | None = None
    sections: list[DataSetSections] | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    skipOffline: bool | None = None
    style: ObjectStyle | None = None
    timelyDays: float | None = None
    translations: list[Translation] | None = None
    user: DataSetUser | None = _Field(default=None, description="A UID reference to a User  ")
    validCompleteOnly: bool | None = None
    version: int | None = None
    workflow: DataSetWorkflow | None = _Field(default=None, description="A UID reference to a DataApprovalWorkflow  ")
