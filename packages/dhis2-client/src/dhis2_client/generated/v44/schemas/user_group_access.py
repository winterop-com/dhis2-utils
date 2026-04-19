"""Generated UserGroupAccess model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class UserGroupAccess(BaseModel):
    """Generated model for DHIS2 `UserGroupAccess`.

    DHIS2 User Group Access - DHIS2 resource (generated from /api/schemas at DHIS2 v44).




    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: str | None = None

    displayName: str | None = None

    id: str | None = None
