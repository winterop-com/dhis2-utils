"""Profile discovery for dhis2-core.

Phase-1 scope: env-based profile resolution only. TOML profile files and
interactive setup are deferred to a later phase.
"""

from __future__ import annotations

import os
from typing import Literal

from pydantic import BaseModel, ConfigDict


class Profile(BaseModel):
    """Resolved DHIS2 connection settings for a single session."""

    model_config = ConfigDict(frozen=True)

    base_url: str
    auth: Literal["pat", "basic"]
    token: str | None = None
    username: str | None = None
    password: str | None = None


class NoProfileError(RuntimeError):
    """Raised when no DHIS2 profile can be resolved from the environment."""


def profile_from_env() -> Profile:
    """Resolve a Profile from environment variables.

    Precedence:
      1. `DHIS2_URL` + `DHIS2_PAT` → PAT auth (preferred).
      2. `DHIS2_URL` + `DHIS2_USERNAME` + `DHIS2_PASSWORD` → Basic auth.
      3. Otherwise raise `NoProfileError`.
    """
    base_url = os.environ.get("DHIS2_URL", "").rstrip("/")
    if not base_url:
        raise NoProfileError(
            "DHIS2_URL is not set. Export DHIS2_URL plus either DHIS2_PAT, or DHIS2_USERNAME + DHIS2_PASSWORD."
        )
    pat = os.environ.get("DHIS2_PAT")
    if pat:
        return Profile(base_url=base_url, auth="pat", token=pat)
    username = os.environ.get("DHIS2_USERNAME")
    password = os.environ.get("DHIS2_PASSWORD")
    if username and password:
        return Profile(base_url=base_url, auth="basic", username=username, password=password)
    raise NoProfileError(
        f"DHIS2_URL={base_url} is set, but no credentials were found. "
        "Export DHIS2_PAT, or DHIS2_USERNAME + DHIS2_PASSWORD."
    )
