"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class MonitoringJobParameters(_BaseModel):
    """OpenAPI schema `MonitoringJobParameters`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    persistResults: bool | None = None
    relativeEnd: int | None = None
    relativeStart: int | None = None
    sendNotifications: bool | None = None
    validationRuleGroups: list[str] | None = None
