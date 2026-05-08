"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .dhis2_info import Dhis2Info


class DataSummary(_BaseModel):
    """OpenAPI schema `DataSummary`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    activeUsers: dict[str, int] | None = _Field(default=None, description="keys are class java.lang.Integer")
    dataValueCount: dict[str, int] | None = _Field(default=None, description="keys are class java.lang.Integer")
    enrollmentCount: dict[str, int] | None = _Field(default=None, description="keys are class java.lang.Integer")
    eventCount: dict[str, int] | None = _Field(default=None, description="keys are class java.lang.Integer")
    logins: dict[str, int] | None = _Field(default=None, description="keys are class java.lang.Integer")
    objectCounts: dict[str, int] | None = None
    singleEventCount: dict[str, int] | None = _Field(default=None, description="keys are class java.lang.Integer")
    system: Dhis2Info | None = None
    trackerEventCount: dict[str, int] | None = _Field(default=None, description="keys are class java.lang.Integer")
    userInvitations: dict[str, int] | None = None
