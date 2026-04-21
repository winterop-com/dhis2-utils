"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class MonitoringJobParameters(_BaseModel):
    """OpenAPI schema `MonitoringJobParameters`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    persistResults: bool | None = None
    relativeEnd: int | None = None
    relativeStart: int | None = None
    sendNotifications: bool | None = None
    validationRuleGroups: list[str] | None = None
