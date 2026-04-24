"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class TrackerUser(_BaseModel):
    """OpenAPI schema `TrackerUser`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    displayName: str | None = None
    firstName: str | None = None
    surname: str | None = None
    uid: str | None = None
    username: str | None = None
