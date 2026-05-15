"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import OrganisationUnitDescendants

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .expression import Expression
    from .sharing import Sharing
    from .translation import Translation


class PredictorParamsCreatedBy(_BaseModel):
    """OpenAPI schema `PredictorParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class PredictorParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `PredictorParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class PredictorParamsOrganisationUnitLevels(_BaseModel):
    """OpenAPI schema `PredictorParamsOrganisationUnitLevels`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class PredictorParamsOutput(_BaseModel):
    """OpenAPI schema `PredictorParamsOutput`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class PredictorParamsOutputCombo(_BaseModel):
    """OpenAPI schema `PredictorParamsOutputCombo`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class PredictorParamsPredictorGroups(_BaseModel):
    """OpenAPI schema `PredictorParamsPredictorGroups`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class PredictorParams(_BaseModel):
    """OpenAPI schema `PredictorParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    annualSampleCount: int | None = None
    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: PredictorParamsCreatedBy | None = None
    description: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    generator: Expression | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: PredictorParamsLastUpdatedBy | None = None
    name: str | None = None
    organisationUnitDescendants: OrganisationUnitDescendants | None = None
    organisationUnitLevels: list[PredictorParamsOrganisationUnitLevels] | None = None
    output: PredictorParamsOutput | None = None
    outputCombo: PredictorParamsOutputCombo | None = None
    periodType: (
        Literal[
            "BiMonthly",
            "BiWeekly",
            "Daily",
            "FinancialApril",
            "FinancialJuly",
            "FinancialNov",
            "FinancialSep",
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
    predictorGroups: list[PredictorParamsPredictorGroups] | None = None
    sampleSkipTest: Expression | None = None
    sequentialSampleCount: int | None = None
    sequentialSkipCount: int | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    translations: list[Translation] | None = None
