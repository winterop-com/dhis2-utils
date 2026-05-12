"""v43-only ProgramsAccessor split surface — labels, change-log, alt enrollment CC.

DHIS2 2.43 added five fields to `Program` that don't exist on v41 / v42:
`enableChangeLog`, `enrollmentsLabel`, `eventsLabel`, `programStagesLabel`,
`enrollmentCategoryCombo`. The accessor exposes them through three
focused setters since they address unrelated concerns:

- `set_labels` — UI label overrides only.
- `set_change_log_enabled` — server-side audit toggle only.
- `set_enrollment_category_combo` — alt-CC reference only.

This module asserts the PUT body shape for each, the omitted-fields
invariant, and the structural "v41 / v42 accessors do not expose these
methods" guard.
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


# ----- set_labels -----------------------------------------------------------


@respx.mock
async def test_set_labels_requires_at_least_one_kwarg() -> None:
    """Calling set_labels with no kwargs raises ValueError."""
    _mock_v43_preamble()
    async with V43Client("https://dhis2.example", auth=_auth()) as client:
        with pytest.raises(ValueError, match="at least one of enrollments_label"):
            await client.programs.set_labels("PRG00000001")


@respx.mock
async def test_set_labels_puts_only_label_fields() -> None:
    """All three label fields land on the PUT body; non-label v43 fields untouched."""
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
            enrollments_label="Visits",
            events_label="Encounters",
            program_stages_label="Stages",
        )

    body = _json.loads(put_route.calls.last.request.content.decode("utf-8"))
    assert body["enrollmentsLabel"] == "Visits"
    assert body["eventsLabel"] == "Encounters"
    assert body["programStagesLabel"] == "Stages"
    # set_labels must NOT touch unrelated v43-only fields.
    assert "enableChangeLog" not in body
    assert "enrollmentCategoryCombo" not in body
    assert put_route.calls.last.request.url.params["mergeMode"] == "REPLACE"


@respx.mock
async def test_set_labels_leaves_omitted_fields_alone() -> None:
    """Passing only one label kwarg doesn't touch the other two."""
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
        await client.programs.set_labels("PRG00000001", program_stages_label="Care Stages")

    body = _json.loads(put_route.calls.last.request.content.decode("utf-8"))
    assert body["programStagesLabel"] == "Care Stages"
    # Pre-existing labels preserved from the read-back; not nulled.
    assert body["enrollmentsLabel"] == "Existing"
    assert body["eventsLabel"] == "Other"


# ----- set_change_log_enabled -----------------------------------------------


@respx.mock
async def test_set_change_log_enabled_puts_only_the_flag() -> None:
    """The change-log toggle PUT body sets exactly one v43-only field."""
    _mock_v43_preamble()
    respx.get("https://dhis2.example/api/programs/PRG00000001").mock(
        return_value=httpx.Response(200, json=_program_payload()),
    )
    put_route = respx.put("https://dhis2.example/api/programs/PRG00000001").mock(
        return_value=httpx.Response(200, json={}),
    )

    async with V43Client("https://dhis2.example", auth=_auth()) as client:
        await client.programs.set_change_log_enabled("PRG00000001", True)

    body = _json.loads(put_route.calls.last.request.content.decode("utf-8"))
    assert body["enableChangeLog"] is True
    assert "enrollmentsLabel" not in body
    assert "eventsLabel" not in body
    assert "programStagesLabel" not in body
    assert "enrollmentCategoryCombo" not in body


@respx.mock
async def test_set_change_log_enabled_false_is_a_real_write() -> None:
    """`enabled=False` writes the flag explicitly (not skipped as None)."""
    _mock_v43_preamble()
    respx.get("https://dhis2.example/api/programs/PRG00000001").mock(
        return_value=httpx.Response(200, json=_program_payload(enableChangeLog=True)),
    )
    put_route = respx.put("https://dhis2.example/api/programs/PRG00000001").mock(
        return_value=httpx.Response(200, json={}),
    )

    async with V43Client("https://dhis2.example", auth=_auth()) as client:
        await client.programs.set_change_log_enabled("PRG00000001", False)

    body = _json.loads(put_route.calls.last.request.content.decode("utf-8"))
    assert body["enableChangeLog"] is False


# ----- set_enrollment_category_combo ----------------------------------------


@respx.mock
async def test_set_enrollment_category_combo_puts_only_the_ref() -> None:
    """The alt-CC setter PUTs only `enrollmentCategoryCombo`."""
    _mock_v43_preamble()
    respx.get("https://dhis2.example/api/programs/PRG00000001").mock(
        return_value=httpx.Response(200, json=_program_payload()),
    )
    put_route = respx.put("https://dhis2.example/api/programs/PRG00000001").mock(
        return_value=httpx.Response(200, json={}),
    )

    async with V43Client("https://dhis2.example", auth=_auth()) as client:
        await client.programs.set_enrollment_category_combo("PRG00000001", "cocAlt000001")

    body = _json.loads(put_route.calls.last.request.content.decode("utf-8"))
    assert body["enrollmentCategoryCombo"] == {"id": "cocAlt000001"}
    assert "enableChangeLog" not in body
    assert "enrollmentsLabel" not in body


@respx.mock
async def test_set_enrollment_category_combo_rejects_empty_uid() -> None:
    """An empty `category_combo_uid` raises ValueError instead of issuing a write."""
    _mock_v43_preamble()
    async with V43Client("https://dhis2.example", auth=_auth()) as client:
        with pytest.raises(ValueError, match="non-empty category_combo_uid"):
            await client.programs.set_enrollment_category_combo("PRG00000001", "")


# ----- v41 / v42 structural guards ------------------------------------------


def test_v43_split_setters_not_on_v42_accessor() -> None:
    """The v42 ProgramsAccessor does not expose any of the three v43-only setters."""
    from dhis2w_client.v42.programs import ProgramsAccessor as V42ProgramsAccessor

    for method in ("set_labels", "set_change_log_enabled", "set_enrollment_category_combo"):
        assert not hasattr(V42ProgramsAccessor, method), (
            f"v42 ProgramsAccessor must not expose {method} — the underlying fields are v43-only."
        )


def test_v43_split_setters_not_on_v41_accessor() -> None:
    """The v41 ProgramsAccessor does not expose any of the three v43-only setters."""
    from dhis2w_client.v41.programs import ProgramsAccessor as V41ProgramsAccessor

    for method in ("set_labels", "set_change_log_enabled", "set_enrollment_category_combo"):
        assert not hasattr(V41ProgramsAccessor, method), (
            f"v41 ProgramsAccessor must not expose {method} — the underlying fields are v43-only."
        )
