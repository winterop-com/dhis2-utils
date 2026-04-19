"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._aliases import Object


class ErrorReport(_BaseModel):
    """OpenAPI schema `ErrorReport`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    args: list[str] | None = None
    errorCode: str | None = None
    errorKlass: str | None = None
    errorProperties: list[Any] | None = None
    errorProperty: str | None = None
    mainId: str | None = None
    mainKlass: str | None = None
    message: str | None = None
    value: Object | None = None
