"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .access import Access
    from .attribute_values import AttributeValues
    from .sharing import Sharing
    from .translation import Translation
    from .user import User


class DimensionalItemObject(_BaseModel):
    """OpenAPI schema `DimensionalItemObject`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: AttributeValues | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: User | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: User | None = None
    name: str | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
