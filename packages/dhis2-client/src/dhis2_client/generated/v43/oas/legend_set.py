"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .legend import Legend
    from .translation import Translation
    from .user_dto import UserDto


class LegendSet(_BaseModel):
    """OpenAPI schema `LegendSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    displayName: str | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    legends: list[Legend] | None = None
    name: str | None = None
    symbolizer: str | None = None
    translations: list[Translation] | None = None
