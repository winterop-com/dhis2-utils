"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class DeletedObject(_BaseModel):
    """OpenAPI schema `DeletedObject`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    code: str | None = None
    deletedAt: datetime | None = None
    deletedBy: str | None = None
    klass: str | None = None
    uid: str | None = None
