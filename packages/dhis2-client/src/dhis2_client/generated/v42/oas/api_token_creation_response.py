"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .error_report import ErrorReport


class ApiTokenCreationResponse(_BaseModel):
    """OpenAPI schema `ApiTokenCreationResponse`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    errorReports: list[ErrorReport] | None = None
    key: str | None = None
    klass: str | None = None
    responseType: str | None = None
    uid: str | None = None
