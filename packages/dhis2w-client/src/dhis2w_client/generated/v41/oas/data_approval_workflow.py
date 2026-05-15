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


class DataApprovalWorkflowCategoryCombo(_BaseModel):
    """A UID reference to a CategoryCombo  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataApprovalWorkflowCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataApprovalWorkflowDataApprovalLevels(_BaseModel):
    """A UID reference to a DataApprovalLevel  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataApprovalWorkflowDataSets(_BaseModel):
    """A UID reference to a DataSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataApprovalWorkflowLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataApprovalWorkflowUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataApprovalWorkflow(_BaseModel):
    """OpenAPI schema `DataApprovalWorkflow`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    categoryCombo: DataApprovalWorkflowCategoryCombo | None = _Field(
        default=None, description="A UID reference to a CategoryCombo  "
    )
    code: str | None = None
    created: datetime | None = None
    createdBy: DataApprovalWorkflowCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    dataApprovalLevels: list[DataApprovalWorkflowDataApprovalLevels] | None = None
    dataSets: list[DataApprovalWorkflowDataSets] | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: DataApprovalWorkflowLastUpdatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    name: str | None = None
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
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
    user: DataApprovalWorkflowUser | None = _Field(default=None, description="A UID reference to a User  ")
