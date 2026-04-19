"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class DHIS2Warning(_BaseModel):
    """OpenAPI schema `Warning`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    message: str | None = None
    trackerType: str | None = None
    uid: str | None = None
    warningCode: str | None = None
