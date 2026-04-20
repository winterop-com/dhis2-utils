"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .sharing_meta import SharingMeta
    from .sharing_object import SharingObject


class SharingInfo(_BaseModel):
    """OpenAPI schema `SharingInfo`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    meta: SharingMeta | None = None
    object: SharingObject | None = None
