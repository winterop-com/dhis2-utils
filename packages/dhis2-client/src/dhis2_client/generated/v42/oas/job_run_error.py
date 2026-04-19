"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class JobRunError(_BaseModel):
    """OpenAPI schema `JobRunError`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    args: list[str] | None = None
    code: str
    id: str | None = None
    message: str
    type: str
