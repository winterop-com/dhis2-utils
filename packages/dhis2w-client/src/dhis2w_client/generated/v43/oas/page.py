"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .program_notification_instance import ProgramNotificationInstance
    from .tracker_pager import TrackerPager


class Page(_BaseModel):
    """OpenAPI schema `Page`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    items: list[ProgramNotificationInstance] | None = None
    pager: TrackerPager | None = None
