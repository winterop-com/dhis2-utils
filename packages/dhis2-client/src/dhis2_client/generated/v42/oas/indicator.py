"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AggregationType

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .base_identifiable_object import BaseIdentifiableObject
    from .legend_set import LegendSet
    from .object_style import ObjectStyle
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto


class Indicator(_BaseModel):
    """OpenAPI schema `Indicator`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    aggregateExportAttributeOptionCombo: str | None = None
    aggregateExportCategoryOptionCombo: str | None = None
    aggregationType: AggregationType | None = None
    annualized: bool | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    dataSets: list[BaseIdentifiableObject] | None = None
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
    indicatorGroups: list[BaseIdentifiableObject] | None = None
    indicatorType: BaseIdentifiableObject | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    legendSet: LegendSet | None = None
    legendSets: list[LegendSet] | None = None
    name: str | None = None
    numerator: str | None = None
    numeratorDescription: str | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    style: ObjectStyle | None = None
    translations: list[Translation] | None = None
    url: str | None = None
