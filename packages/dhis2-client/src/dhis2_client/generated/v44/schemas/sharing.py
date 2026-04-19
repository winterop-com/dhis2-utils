"""Generated Sharing model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference


class Sharing(BaseModel):
    """Generated model for DHIS2 `Sharing`.

    DHIS2 Sharing - DHIS2 resource (generated from /api/schemas at DHIS2 v44).


    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    owner: str | None = None
    publicAccess: str | None = None
    userGroups: Any | None = Field(default=None, description="Reference to Map. Read-only (inverse side).")
    users: Any | None = Field(default=None, description="Reference to Map. Read-only (inverse side).")
