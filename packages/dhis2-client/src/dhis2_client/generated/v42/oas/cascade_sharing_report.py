"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .error_report import ErrorReport
    from .id_object import IdObject


class CascadeSharingReport(_BaseModel):
    """OpenAPI schema `CascadeSharingReport`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    countUpdatedDashboardItems: int
    errorReports: list[ErrorReport] | None = None
    updateObjects: dict[str, list[IdObject]] | None = None
