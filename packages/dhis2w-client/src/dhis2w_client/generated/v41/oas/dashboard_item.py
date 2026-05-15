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


class DashboardItemCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DashboardItemEventChart(_BaseModel):
    """A UID reference to a EventChart  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DashboardItemEventReport(_BaseModel):
    """A UID reference to a EventReport  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DashboardItemEventVisualization(_BaseModel):
    """A UID reference to a EventVisualization  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DashboardItemLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DashboardItemMap(_BaseModel):
    """A UID reference to a Map  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DashboardItemReports(_BaseModel):
    """A UID reference to a Report  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DashboardItemResources(_BaseModel):
    """A UID reference to a Document  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DashboardItemUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DashboardItemUsers(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DashboardItemVisualization(_BaseModel):
    """A UID reference to a Visualization  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DashboardItem(_BaseModel):
    """OpenAPI schema `DashboardItem`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    appKey: str | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    contentCount: int | None = None
    created: datetime | None = None
    createdBy: DashboardItemCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    displayName: str | None = None
    eventChart: DashboardItemEventChart | None = _Field(default=None, description="A UID reference to a EventChart  ")
    eventReport: DashboardItemEventReport | None = _Field(
        default=None, description="A UID reference to a EventReport  "
    )
    eventVisualization: DashboardItemEventVisualization | None = _Field(
        default=None, description="A UID reference to a EventVisualization  "
    )
    favorite: bool | None = None
    favorites: list[str] | None = None
    height: int | None = None
    href: str | None = None
    id: str | None = None
    interpretationCount: int | None = None
    interpretationLikeCount: int | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: DashboardItemLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    map: DashboardItemMap | None = _Field(default=None, description="A UID reference to a Map  ")
    messages: bool | None = None
    name: str | None = None
    reports: list[DashboardItemReports] | None = None
    resources: list[DashboardItemResources] | None = None
    shape: Literal["NORMAL", "DOUBLE_WIDTH", "FULL_WIDTH"] | None = None
    sharing: Sharing | None = None
    text: str | None = None
    translations: list[Translation] | None = None
    type: (
        Literal[
            "VISUALIZATION",
            "EVENT_VISUALIZATION",
            "EVENT_CHART",
            "MAP",
            "EVENT_REPORT",
            "USERS",
            "REPORTS",
            "RESOURCES",
            "TEXT",
            "MESSAGES",
            "APP",
        ]
        | None
    ) = None
    user: DashboardItemUser | None = _Field(default=None, description="A UID reference to a User  ")
    users: list[DashboardItemUsers] | None = None
    visualization: DashboardItemVisualization | None = _Field(
        default=None, description="A UID reference to a Visualization  "
    )
    width: int | None = None
    x: int | None = None
    y: int | None = None
