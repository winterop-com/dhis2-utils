"""Unit tests for dhis2-core profile resolution."""

from __future__ import annotations

import pytest
from dhis2_core.profile import NoProfileError, profile_from_env


def test_profile_from_env_pat(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DHIS2_URL", "http://localhost:8080/")
    monkeypatch.setenv("DHIS2_PAT", "d2p_test")
    monkeypatch.delenv("DHIS2_USERNAME", raising=False)
    monkeypatch.delenv("DHIS2_PASSWORD", raising=False)
    profile = profile_from_env()
    assert profile.base_url == "http://localhost:8080"
    assert profile.auth == "pat"
    assert profile.token == "d2p_test"


def test_profile_from_env_basic(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DHIS2_URL", "http://localhost:8080")
    monkeypatch.delenv("DHIS2_PAT", raising=False)
    monkeypatch.setenv("DHIS2_USERNAME", "admin")
    monkeypatch.setenv("DHIS2_PASSWORD", "district")
    profile = profile_from_env()
    assert profile.auth == "basic"
    assert profile.username == "admin"
    assert profile.password == "district"


def test_profile_from_env_pat_beats_basic(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DHIS2_URL", "http://localhost:8080")
    monkeypatch.setenv("DHIS2_PAT", "d2p_token")
    monkeypatch.setenv("DHIS2_USERNAME", "admin")
    monkeypatch.setenv("DHIS2_PASSWORD", "district")
    profile = profile_from_env()
    assert profile.auth == "pat"


def test_profile_from_env_missing_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DHIS2_URL", raising=False)
    monkeypatch.delenv("DHIS2_PAT", raising=False)
    with pytest.raises(NoProfileError):
        profile_from_env()


def test_profile_from_env_missing_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DHIS2_URL", "http://localhost:8080")
    monkeypatch.delenv("DHIS2_PAT", raising=False)
    monkeypatch.delenv("DHIS2_USERNAME", raising=False)
    monkeypatch.delenv("DHIS2_PASSWORD", raising=False)
    with pytest.raises(NoProfileError):
        profile_from_env()
