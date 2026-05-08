"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import Status


class WebResponse(_BaseModel):
    """OpenAPI schema `WebResponse`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    code: int | None = None
    errorCode: str | None = None
    message: str | None = None
    status: Status | None = None
