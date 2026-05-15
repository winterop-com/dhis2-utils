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
    from .sharing import Sharing
    from .translation import Translation


class PredictorCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class PredictorLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class PredictorOrganisationUnitLevels(_BaseModel):
    """A UID reference to a OrganisationUnitLevel  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class PredictorOutput(_BaseModel):
    """A UID reference to a DataElement  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class PredictorOutputCombo(_BaseModel):
    """A UID reference to a CategoryOptionCombo  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class PredictorPredictorGroups(_BaseModel):
    """A UID reference to a PredictorGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class PredictorUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class Predictor(_BaseModel):
    """OpenAPI schema `Predictor`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    annualSampleCount: int | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: PredictorCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    description: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    generator: Expression | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: PredictorLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    name: str | None = None
    organisationUnitDescendants: Literal["SELECTED", "DESCENDANTS"] | None = None
    organisationUnitLevels: list[PredictorOrganisationUnitLevels] | None = None
    output: PredictorOutput | None = _Field(default=None, description="A UID reference to a DataElement  ")
    outputCombo: PredictorOutputCombo | None = _Field(
        default=None, description="A UID reference to a CategoryOptionCombo  "
    )
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
    predictorGroups: list[PredictorPredictorGroups] | None = None
    sampleSkipTest: Expression | None = None
    sequentialSampleCount: int | None = None
    sequentialSkipCount: int | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    translations: list[Translation] | None = None
    user: PredictorUser | None = _Field(default=None, description="A UID reference to a User  ")
