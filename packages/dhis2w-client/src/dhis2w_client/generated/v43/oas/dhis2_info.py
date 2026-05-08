"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class Dhis2Info(_BaseModel):
    """OpenAPI schema `Dhis2Info`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    buildTime: datetime | None = None
    revision: str | None = None
    serverDate: datetime | None = None
    systemId: str | None = None
    version: str | None = None
