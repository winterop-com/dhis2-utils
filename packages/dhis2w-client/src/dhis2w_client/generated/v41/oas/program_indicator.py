"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .analytics_period_boundary import AnalyticsPeriodBoundary
    from .attribute_value import AttributeValue
    from .object_style import ObjectStyle
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class ProgramIndicatorCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramIndicatorLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramIndicatorLegendSet(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramIndicatorLegendSets(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramIndicatorProgram(_BaseModel):
    """A UID reference to a Program  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramIndicatorProgramIndicatorGroups(_BaseModel):
    """A UID reference to a ProgramIndicatorGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramIndicatorUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramIndicator(_BaseModel):
    """OpenAPI schema `ProgramIndicator`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    aggregateExportAttributeOptionCombo: str | None = None
    aggregateExportCategoryOptionCombo: str | None = None
    aggregationType: str | None = None
    analyticsPeriodBoundaries: list[AnalyticsPeriodBoundary] | None = None
    analyticsType: str | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ProgramIndicatorCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    decimals: int | None = None
    description: str | None = None
    dimensionItem: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayInForm: bool | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    expression: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    filter: str | None = None
    formName: str | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramIndicatorLastUpdatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    legendSet: ProgramIndicatorLegendSet | None = _Field(default=None, description="A UID reference to a LegendSet  ")
    legendSets: list[ProgramIndicatorLegendSets] | None = None
    name: str | None = None
    orgUnitField: str | None = None
    program: ProgramIndicatorProgram | None = _Field(default=None, description="A UID reference to a Program  ")
    programIndicatorGroups: list[ProgramIndicatorProgramIndicatorGroups] | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    style: ObjectStyle | None = None
    translations: list[Translation] | None = None
    user: ProgramIndicatorUser | None = _Field(default=None, description="A UID reference to a User  ")
