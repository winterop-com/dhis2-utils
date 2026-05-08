"""Shared fixtures for dhis2-codegen tests (mirror of dhis2-client's play fixtures)."""

from __future__ import annotations

import os

import pytest


@pytest.fixture(scope="session")
def play_url() -> str:
    """Base URL of the DHIS2 play instance used by integration tests."""
    return os.environ.get("DHIS2_PLAY_URL", "https://play.im.dhis2.org/dev").rstrip("/")


@pytest.fixture(scope="session")
def play_username() -> str:
    """Username for the DHIS2 play instance."""
    return os.environ.get("DHIS2_PLAY_USER", "system")


@pytest.fixture(scope="session")
def play_password() -> str:
    """Password for the DHIS2 play instance."""
    return os.environ.get("DHIS2_PLAY_PASS", "System123")
