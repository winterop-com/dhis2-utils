"""v43-only ProgramsAccessor.set_labels — respx-mocked.

Covers the v43 Program schema additions (enableChangeLog, enrollmentsLabel,
eventsLabel, programStagesLabel, enrollmentCategoryCombo) that don't exist
on v41 / v42 schemas. Asserts the PUT body carries the new fields and the
re-fetch round-trip preserves them.
"""

from __future__ import annotations

import json as _json
from typing import Any

import httpx
import pytest
import respx
from dhis2w_client import BasicAuth
from dhis2w_client.v43.client import Dhis2Client as V43Client


def _auth() -> BasicAuth:
    """Throwaway BasicAuth for connect tests."""
    return BasicAuth(username="admin", password="district")


def _mock_redirect_probe() -> None:
    """Mock the unauthenticated canonical-URL resolution probe."""
    respx.get("https://dhis2.example/").mock(return_value=httpx.Response(200, text="<html></html>"))


def _mock_v43_preamble() -> None:
    """Connect-side mocks: redirect probe + 2.43.0 systemInfo."""
    _mock_redirect_probe()
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.43.0"})
    )


def _program_payload(**overrides: Any) -> dict[str, Any]:
    """Minimal Program payload for the GET-before-PUT round-trip."""
    base: dict[str, Any] = {
        "id": "PRG00000001",
        "name": "ANC",
        "shortName": "ANC",
        "programType": "WITH_REGISTRATION",
        "trackedEntityType": {"id": "TET00000001", "name": "Person"},
        "categoryCombo": {"id": "ccDefault001", "name": "default"},
    }
    base.update(overrides)
    return base


@respx.mock
async def test_set_labels_requires_at_least_one_kwarg() -> None:
    """Calling set_labels with no kwargs raises ValueError."""
    _mock_v43_preamble()
    async with V43Client("https://dhis2.example", auth=_auth()) as client:
        with pytest.raises(ValueError, match="at least one"):
            await client.programs.set_labels("PRG00000001")


@respx.mock
async def test_set_labels_puts_v43_fields_into_program_body() -> None:
    """All five v43-only fields land on the PUT body verbatim."""
    _mock_v43_preamble()
    respx.get("https://dhis2.example/api/programs/PRG00000001").mock(
        return_value=httpx.Response(200, json=_program_payload()),
    )
    put_route = respx.put("https://dhis2.example/api/programs/PRG00000001").mock(
        return_value=httpx.Response(200, json={}),
    )

    async with V43Client("https://dhis2.example", auth=_auth()) as client:
        await client.programs.set_labels(
            "PRG00000001",
            enable_change_log=True,
            enrollments_label="Visits",
            events_label="Encounters",
            program_stages_label="Stages",
            enrollment_category_combo_uid="cocAlt000001",
        )

    body = _json.loads(put_route.calls.last.request.content.decode("utf-8"))
    assert body["enableChangeLog"] is True
    assert body["enrollmentsLabel"] == "Visits"
    assert body["eventsLabel"] == "Encounters"
    assert body["programStagesLabel"] == "Stages"
    assert body["enrollmentCategoryCombo"] == {"id": "cocAlt000001"}
    assert put_route.calls.last.request.url.params["mergeMode"] == "REPLACE"


@respx.mock
async def test_set_labels_leaves_omitted_fields_alone() -> None:
    """Passing only enable_change_log doesn't touch the label fields."""
    _mock_v43_preamble()
    respx.get("https://dhis2.example/api/programs/PRG00000001").mock(
        return_value=httpx.Response(
            200,
            json=_program_payload(enrollmentsLabel="Existing", eventsLabel="Other"),
        ),
    )
    put_route = respx.put("https://dhis2.example/api/programs/PRG00000001").mock(
        return_value=httpx.Response(200, json={}),
    )

    async with V43Client("https://dhis2.example", auth=_auth()) as client:
        await client.programs.set_labels("PRG00000001", enable_change_log=False)

    body = _json.loads(put_route.calls.last.request.content.decode("utf-8"))
    assert body["enableChangeLog"] is False
    # Pre-existing fields preserved from the read-back; not nulled.
    assert body["enrollmentsLabel"] == "Existing"
    assert body["eventsLabel"] == "Other"
    assert "programStagesLabel" not in body


def test_set_labels_is_not_on_v42_accessor() -> None:
    """The v42 ProgramsAccessor does not expose set_labels — the fields don't exist on v42."""
    from dhis2w_client.v42.programs import ProgramsAccessor as V42ProgramsAccessor

    assert not hasattr(V42ProgramsAccessor, "set_labels"), (
        "v42 ProgramsAccessor must not expose set_labels — the underlying fields are v43-only."
    )


def test_set_labels_is_not_on_v41_accessor() -> None:
    """The v41 ProgramsAccessor does not expose set_labels — the fields don't exist on v41."""
    from dhis2w_client.v41.programs import ProgramsAccessor as V41ProgramsAccessor

    assert not hasattr(V41ProgramsAccessor, "set_labels"), (
        "v41 ProgramsAccessor must not expose set_labels — the underlying fields are v43-only."
    )
