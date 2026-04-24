"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .app_dhis import AppDhis


class AppActivities(_BaseModel):
    """OpenAPI schema `AppActivities`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    dhis: AppDhis | None = None
