"""Generated DHIS2 v44 shared types. Do not edit by hand."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal `{id: str}` reference to another DHIS2 object.

    Every typed schema with a foreign-key field (`categoryCombo`, `parent`,
    `dataElement`, ...) uses this as the nested shape. DHIS2 accepts extras
    like `{id, name, code}` when sending references back, so `extra="allow"`
    preserves whatever the server returns.
    """

    model_config = ConfigDict(extra="allow")

    id: str | None = None
