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


class AnalyticsTableHookCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class AnalyticsTableHookLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class AnalyticsTableHookUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class AnalyticsTableHook(_BaseModel):
    """OpenAPI schema `AnalyticsTableHook`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    analyticsTableType: (
        Literal[
            "DATA_VALUE",
            "COMPLETENESS",
            "COMPLETENESS_TARGET",
            "ORG_UNIT_TARGET",
            "VALIDATION_RESULT",
            "EVENT",
            "ENROLLMENT",
            "OWNERSHIP",
            "TRACKED_ENTITY_INSTANCE_EVENTS",
            "TRACKED_ENTITY_INSTANCE_ENROLLMENTS",
            "TRACKED_ENTITY_INSTANCE",
        ]
        | None
    ) = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: AnalyticsTableHookCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: AnalyticsTableHookLastUpdatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    name: str | None = None
    phase: Literal["RESOURCE_TABLE_POPULATED", "ANALYTICS_TABLE_POPULATED"] | None = None
    resourceTableType: (
        Literal[
            "ORG_UNIT_STRUCTURE",
            "DATA_SET_ORG_UNIT_CATEGORY",
            "CATEGORY_OPTION_COMBO_NAME",
            "DATA_ELEMENT_GROUP_SET_STRUCTURE",
            "INDICATOR_GROUP_SET_STRUCTURE",
            "ORG_UNIT_GROUP_SET_STRUCTURE",
            "CATEGORY_STRUCTURE",
            "DATA_ELEMENT_STRUCTURE",
            "PERIOD_STRUCTURE",
            "DATE_PERIOD_STRUCTURE",
            "DATA_ELEMENT_CATEGORY_OPTION_COMBO",
            "DATA_APPROVAL_REMAP_LEVEL",
            "DATA_APPROVAL_MIN_LEVEL",
        ]
        | None
    ) = None
    sharing: Sharing | None = None
    sql: str | None = None
    translations: list[Translation] | None = None
    user: AnalyticsTableHookUser | None = _Field(default=None, description="A UID reference to a User  ")
