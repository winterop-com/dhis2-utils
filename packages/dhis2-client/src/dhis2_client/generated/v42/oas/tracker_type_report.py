"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import TrackerType

if TYPE_CHECKING:
    from .entity import Entity
    from .tracker_stats import TrackerStats


class TrackerTypeReport(_BaseModel):
    """OpenAPI schema `TrackerTypeReport`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    objectReports: list[Entity] | None = None
    stats: TrackerStats | None = None
    trackerType: TrackerType | None = None
