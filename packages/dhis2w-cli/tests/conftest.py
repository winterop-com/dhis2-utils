"""Pytest fixtures for dhis2w-cli tests — mirrors dhis2w-client's seeded-env loading."""

from __future__ import annotations

import os
from pathlib import Path

import pytest


def _load_seeded_env(start: Path) -> None:
    """Load `infra/home/credentials/.env.auth` into os.environ if present (setdefault)."""
    for parent in [start, *start.parents]:
        candidate = parent / "infra" / "home" / "credentials" / ".env.auth"
        if candidate.exists():
            for raw_line in candidate.read_text(encoding="utf-8").splitlines():
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())
            return


_load_seeded_env(Path(__file__).resolve())


@pytest.fixture(scope="session")
def local_url() -> str:
    """Base URL of the local DHIS2 instance (defaults to seeded DHIS2_URL)."""
    return os.environ.get("DHIS2_URL", "http://localhost:8080").rstrip("/")


@pytest.fixture(scope="session")
def local_pat() -> str | None:
    """Seeded default PAT from `infra/home/credentials/.env.auth` (or None)."""
    return os.environ.get("DHIS2_PAT")
