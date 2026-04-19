"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AnalyticsFavoriteType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .data_set_params import DataSetParams
    from .event_chart_params import EventChartParams
    from .event_report_params import EventReportParams
    from .event_visualization_params import EventVisualizationParams
    from .map_params import MapParams
    from .mention import Mention
    from .organisation_unit_params import OrganisationUnitParams
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto
    from .visualization_params import VisualizationParams


class InterpretationParamsComments(_BaseModel):
    """OpenAPI schema `InterpretationParamsComments`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class InterpretationParamsCreatedBy(_BaseModel):
    """OpenAPI schema `InterpretationParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class InterpretationParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `InterpretationParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class InterpretationParams(_BaseModel):
    """OpenAPI schema `InterpretationParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    comments: list[InterpretationParamsComments] | None = None
    created: datetime | None = None
    createdBy: InterpretationParamsCreatedBy | None = None
    dataSet: DataSetParams | None = None
    displayName: str | None = None
    eventChart: EventChartParams | None = None
    eventReport: EventReportParams | None = None
    eventVisualization: EventVisualizationParams | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: InterpretationParamsLastUpdatedBy | None = None
    likedBy: list[UserDto] | None = None
    likes: int
    map: MapParams | None = None
    mentions: list[Mention] | None = None
    organisationUnit: OrganisationUnitParams | None = None
    period: str | None = None
    sharing: Sharing | None = None
    text: str | None = None
    translations: list[Translation] | None = None
    type: AnalyticsFavoriteType
    visualization: VisualizationParams | None = None
