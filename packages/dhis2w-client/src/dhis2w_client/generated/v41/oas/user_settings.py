"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class UserSettings(_BaseModel):
    """OpenAPI schema `UserSettings`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    analysisDisplayProperty: str | None = None
    dbLocale: str | None = None
    messageEmailNotification: bool | None = None
    messageSmsNotification: bool | None = None
    style: str | None = None
    trackerDashboardLayout: str | None = None
    uiLocale: str | None = None
