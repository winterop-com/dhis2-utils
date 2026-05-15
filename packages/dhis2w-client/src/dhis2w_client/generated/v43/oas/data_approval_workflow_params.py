"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .category_combo_params import CategoryComboParams


class DataApprovalWorkflowParamsCreatedBy(_BaseModel):
    """OpenAPI schema `DataApprovalWorkflowParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataApprovalWorkflowParamsDataApprovalLevels(_BaseModel):
    """OpenAPI schema `DataApprovalWorkflowParamsDataApprovalLevels`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataApprovalWorkflowParamsDataSets(_BaseModel):
    """OpenAPI schema `DataApprovalWorkflowParamsDataSets`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataApprovalWorkflowParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `DataApprovalWorkflowParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataApprovalWorkflowParams(_BaseModel):
    """OpenAPI schema `DataApprovalWorkflowParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    categoryCombo: CategoryComboParams | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: DataApprovalWorkflowParamsCreatedBy | None = None
    dataApprovalLevels: list[DataApprovalWorkflowParamsDataApprovalLevels] | None = None
    dataSets: list[DataApprovalWorkflowParamsDataSets] | None = None
    displayName: str | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: DataApprovalWorkflowParamsLastUpdatedBy | None = None
    name: str | None = None
    periodType: (
        Literal[
            "BiMonthly",
            "BiWeekly",
            "Daily",
            "FinancialFeb",
            "FinancialApril",
            "FinancialJuly",
            "FinancialAug",
            "FinancialSep",
            "FinancialOct",
            "FinancialNov",
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
            "WeeklyFriday",
            "WeeklyWednesday",
            "Yearly",
        ]
        | None
    ) = None
