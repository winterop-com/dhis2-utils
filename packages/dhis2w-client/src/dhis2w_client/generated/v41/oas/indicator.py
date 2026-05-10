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
    from .attribute_value import AttributeValue
    from .object_style import ObjectStyle
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class IndicatorCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IndicatorDataSets(_BaseModel):
    """A UID reference to a DataSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IndicatorIndicatorGroups(_BaseModel):
    """A UID reference to a IndicatorGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IndicatorIndicatorType(_BaseModel):
    """A UID reference to a IndicatorType  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IndicatorLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IndicatorLegendSet(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IndicatorLegendSets(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IndicatorUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class Indicator(_BaseModel):
    """OpenAPI schema `Indicator`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    aggregateExportAttributeOptionCombo: str | None = None
    aggregateExportCategoryOptionCombo: str | None = None
    aggregationType: str | None = None
    annualized: bool | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: IndicatorCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    dataSets: list[IndicatorDataSets] | None = None
    decimals: int | None = None
    denominator: str | None = None
    denominatorDescription: str | None = None
    description: str | None = None
    dimensionItem: str | None = None
    displayDenominatorDescription: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayNumeratorDescription: str | None = None
    displayShortName: str | None = None
    explodedDenominator: str | None = None
    explodedNumerator: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    href: str | None = None
    id: str | None = None
    indicatorGroups: list[IndicatorIndicatorGroups] | None = None
    indicatorType: IndicatorIndicatorType | None = _Field(
        default=None, description="A UID reference to a IndicatorType  "
    )
    lastUpdated: datetime | None = None
    lastUpdatedBy: IndicatorLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    legendSet: IndicatorLegendSet | None = _Field(default=None, description="A UID reference to a LegendSet  ")
    legendSets: list[IndicatorLegendSets] | None = None
    name: str | None = None
    numerator: str | None = None
    numeratorDescription: str | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    style: ObjectStyle | None = None
    translations: list[Translation] | None = None
    url: str | None = None
    user: IndicatorUser | None = _Field(default=None, description="A UID reference to a User  ")
