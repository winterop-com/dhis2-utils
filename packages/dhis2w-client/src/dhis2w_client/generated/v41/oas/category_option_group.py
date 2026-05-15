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
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class CategoryOptionGroupCategoryOptions(_BaseModel):
    """A UID reference to a CategoryOption  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionGroupCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionGroupGroupSets(_BaseModel):
    """A UID reference to a CategoryOptionGroupSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionGroupLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionGroupLegendSet(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionGroupLegendSets(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionGroupUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionGroup(_BaseModel):
    """OpenAPI schema `CategoryOptionGroup`."""

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
    categoryOptions: list[CategoryOptionGroupCategoryOptions] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: CategoryOptionGroupCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    dataDimensionType: Literal["DISAGGREGATION", "ATTRIBUTE"] | None = None
    description: str | None = None
    dimensionItem: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    groupSets: list[CategoryOptionGroupGroupSets] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: CategoryOptionGroupLastUpdatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    legendSet: CategoryOptionGroupLegendSet | None = _Field(
        default=None, description="A UID reference to a LegendSet  "
    )
    legendSets: list[CategoryOptionGroupLegendSets] | None = None
    name: str | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    translations: list[Translation] | None = None
    user: CategoryOptionGroupUser | None = _Field(default=None, description="A UID reference to a User  ")
