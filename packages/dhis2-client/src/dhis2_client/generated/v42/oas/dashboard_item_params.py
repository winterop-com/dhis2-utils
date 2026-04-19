"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import DashboardItemShape, DashboardItemType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .event_chart_params import EventChartParams
    from .event_report_params import EventReportParams
    from .event_visualization_params import EventVisualizationParams
    from .map_params import MapParams
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto
    from .visualization_params import VisualizationParams


class DashboardItemParamsCreatedBy(_BaseModel):
    """OpenAPI schema `DashboardItemParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class DashboardItemParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `DashboardItemParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class DashboardItemParamsReports(_BaseModel):
    """OpenAPI schema `DashboardItemParamsReports`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class DashboardItemParamsResources(_BaseModel):
    """OpenAPI schema `DashboardItemParamsResources`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class DashboardItemParams(_BaseModel):
    """OpenAPI schema `DashboardItemParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    appKey: str | None = None
    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    contentCount: int
    created: datetime | None = None
    createdBy: DashboardItemParamsCreatedBy | None = None
    displayName: str | None = None
    eventChart: EventChartParams | None = None
    eventReport: EventReportParams | None = None
    eventVisualization: EventVisualizationParams | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    height: int | None = None
    id: str | None = None
    interpretationCount: int
    interpretationLikeCount: int
    lastUpdated: datetime | None = None
    lastUpdatedBy: DashboardItemParamsLastUpdatedBy | None = None
    map: MapParams | None = None
    messages: bool | None = None
    name: str | None = None
    reports: list[DashboardItemParamsReports] | None = None
    resources: list[DashboardItemParamsResources] | None = None
    shape: DashboardItemShape
    sharing: Sharing | None = None
    text: str | None = None
    translations: list[Translation] | None = None
    type: DashboardItemType
    users: list[UserDto] | None = None
    visualization: VisualizationParams | None = None
    width: int | None = None
    x: int | None = None
    y: int | None = None
