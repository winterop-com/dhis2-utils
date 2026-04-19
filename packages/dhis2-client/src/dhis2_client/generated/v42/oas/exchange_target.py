"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import TargetType

if TYPE_CHECKING:
    from .api import Api
    from .target_request import TargetRequest


class ExchangeTarget(_BaseModel):
    """OpenAPI schema `ExchangeTarget`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    api: Api | None = None
    request: TargetRequest | None = None
    type: TargetType | None = None
