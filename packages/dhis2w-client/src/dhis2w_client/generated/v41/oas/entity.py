"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .tracker_import_error import TrackerImportError


class Entity(_BaseModel):
    """OpenAPI schema `Entity`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    errorReports: list[TrackerImportError] | None = None
    trackerType: str | None = None
    uid: str | None = None
