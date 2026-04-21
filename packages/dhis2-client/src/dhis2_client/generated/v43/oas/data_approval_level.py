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
    from .category_option_group_set import CategoryOptionGroupSet
    from .user_dto import UserDto


class DataApprovalLevel(_BaseModel):
    """OpenAPI schema `DataApprovalLevel`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    categoryOptionGroupSet: CategoryOptionGroupSet | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    displayName: str | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    level: int | None = None
    orgUnitLevel: int | None = None
    orgUnitLevelName: str | None = None
