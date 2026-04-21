"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .org_unit_info import OrgUnitInfo
    from .profile_item import ProfileItem


class OrgUnitProfileData(_BaseModel):
    """OpenAPI schema `OrgUnitProfileData`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributes: list[ProfileItem] | None = None
    dataItems: list[ProfileItem] | None = None
    groupSets: list[ProfileItem] | None = None
    info: OrgUnitInfo | None = None
