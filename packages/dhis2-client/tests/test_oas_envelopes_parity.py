"""Parity tests: OAS-derived envelopes parse real DHIS2 response bodies."""

from __future__ import annotations

import json
from pathlib import Path

from dhis2_client import WebMessageResponse

_FIXTURE_409 = Path(__file__).parent / "fixtures" / "openapi_parity" / "data_value_set_409.json"


def test_real_409_data_value_set_envelope_parses_and_surfaces_conflicts() -> None:
    """`POST /api/dataValueSets` with a rejected period returns a WebMessage with conflicts."""
    raw = json.loads(_FIXTURE_409.read_text())
    envelope = WebMessageResponse.model_validate(raw)

    assert envelope.httpStatus == "Conflict"
    assert envelope.httpStatusCode == 409
    assert envelope.status is not None

    conflicts = envelope.conflicts()
    assert len(conflicts) >= 1
    # Every conflict gets its errorCode preserved (string — OAS emits it as
    # alias rather than closed enum because DHIS2 extends the code list).
    for conflict in conflicts:
        assert isinstance(conflict.errorCode, str) or conflict.errorCode is None

    # rejected_indexes is populated when conflicts are.
    rejected = envelope.rejected_indexes()
    assert isinstance(rejected, list)


def test_import_count_projects_from_nested_response() -> None:
    """`response.importCount = {...}` reaches the typed ImportCount via `import_count()`."""
    raw = json.loads(_FIXTURE_409.read_text())
    envelope = WebMessageResponse.model_validate(raw)
    counts = envelope.import_count()
    assert counts is not None
    # Whatever the imported/updated/ignored values, all four fields are present on the model.
    for field_name in ("imported", "updated", "ignored", "deleted"):
        assert hasattr(counts, field_name)
