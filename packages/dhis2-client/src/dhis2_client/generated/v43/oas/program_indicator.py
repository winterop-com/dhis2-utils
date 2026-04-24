"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AggregationType, AnalyticsType

if TYPE_CHECKING:
    from .access import Access
    from .analytics_period_boundary import AnalyticsPeriodBoundary
    from .attribute_value import AttributeValue
    from .identifiable_object import IdentifiableObject
    from .legend_set import LegendSet
    from .object_style import ObjectStyle
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto


class ProgramIndicator(_BaseModel):
    """OpenAPI schema `ProgramIndicator`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    aggregateExportAttributeOptionCombo: str | None = None
    aggregateExportCategoryOptionCombo: str | None = None
    aggregateExportDataElement: str | None = None
    aggregationType: AggregationType | None = None
    analyticsPeriodBoundaries: list[AnalyticsPeriodBoundary] | None = None
    analyticsType: AnalyticsType | None = None
    attributeCombo: IdentifiableObject | None = None
    attributeValues: list[AttributeValue] | None = None
    categoryCombo: IdentifiableObject | None = None
    categoryMappingIds: list[str] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
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
    lastUpdatedBy: UserDto | None = None
    legendSet: LegendSet | None = None
    legendSets: list[LegendSet] | None = None
    name: str | None = None
    orgUnitField: str | None = None
    program: IdentifiableObject | None = None
    programIndicatorGroups: list[IdentifiableObject] | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    style: ObjectStyle | None = None
    translations: list[Translation] | None = None
