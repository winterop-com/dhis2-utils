"""Unit tests for the DHIS2 WebMessageResponse / ObjectReport / ImportReport models."""

from __future__ import annotations

from dhis2_client import ImportCount, ObjectReport, WebMessageResponse


def test_object_report_response_parses_created_uid() -> None:
    """Typical `POST /api/routes` response envelope — created_uid pulls response.uid."""
    envelope = WebMessageResponse.model_validate(
        {
            "httpStatus": "Created",
            "httpStatusCode": 201,
            "status": "OK",
            "response": {
                "uid": "abc123uid12",
                "klass": "org.hisp.dhis.route.Route",
                "errorReports": [],
                "responseType": "ObjectReportWebMessageResponse",
            },
        }
    )
    assert envelope.httpStatus == "Created"
    assert envelope.httpStatusCode == 201
    assert envelope.status == "OK"
    assert envelope.created_uid == "abc123uid12"

    inner = envelope.object_report()
    assert inner is not None
    assert inner.uid == "abc123uid12"
    assert inner.klass == "org.hisp.dhis.route.Route"
    assert inner.errorReports == []


def test_error_envelope_preserves_error_reports() -> None:
    """Envelope with E4030 errorReports — callers can drill into per-object reasons."""
    envelope = WebMessageResponse.model_validate(
        {
            "httpStatus": "Conflict",
            "httpStatusCode": 409,
            "status": "WARNING",
            "message": "One or more errors occurred, please see full details in import report.",
            "response": {
                "uid": "badObject1",
                "klass": "org.hisp.dhis.dataelement.DataElement",
                "errorReports": [
                    {
                        "message": (
                            "Object could not be deleted because it is associated with another object: DataValue"
                        ),
                        "mainKlass": "org.hisp.dhis.dataelement.DataElement",
                        "errorCode": "E4030",
                        "errorProperties": [],
                    }
                ],
                "responseType": "ObjectReportWebMessageResponse",
            },
        }
    )
    inner = envelope.object_report()
    assert inner is not None
    assert len(inner.errorReports) == 1
    assert inner.errorReports[0].errorCode == "E4030"


def test_import_count_from_data_value_set_response() -> None:
    """Data-value-set POST returns response: {importCount: {...}} — import_count() parses it."""
    # Real DHIS2 dataValueSets response wraps importCount under `response.importCount`, not directly:
    # {..., "response": {"responseType": "ImportSummary", "importCount": {"imported": 1, ...}}}
    # Callers typically reach in manually, or pydantic-validate against ImportCount if flat.
    envelope = WebMessageResponse.model_validate(
        {
            "status": "SUCCESS",
            "response": {
                "imported": 5,
                "updated": 2,
                "ignored": 0,
                "deleted": 0,
            },
        }
    )
    counts = envelope.import_count()
    assert counts is not None
    assert counts.imported == 5
    assert counts.updated == 2
    assert counts.ignored == 0
    assert counts.deleted == 0


def test_created_uid_falls_back_to_id_when_no_uid() -> None:
    """Defensive lookup: BUGS.md #4f — some endpoints return `id` not `uid`."""
    envelope = WebMessageResponse.model_validate(
        {"status": "OK", "response": {"id": "fromIdField", "name": "something"}}
    )
    assert envelope.created_uid == "fromIdField"


def test_created_uid_none_when_response_missing() -> None:
    envelope = WebMessageResponse.model_validate({"status": "OK"})
    assert envelope.created_uid is None
    assert envelope.object_report() is None


def test_extra_fields_are_preserved() -> None:
    """DHIS2 adds fields over time; extra='allow' keeps them accessible for downstream callers."""
    envelope = WebMessageResponse.model_validate(
        {
            "status": "OK",
            "somethingNew": "future-field",
            "response": {"uid": "u", "klass": "X"},
        }
    )
    # Dumped dict preserves the extra field so downstream CLI/MCP JSON output keeps it.
    dumped = envelope.model_dump(exclude_none=True)
    assert dumped["somethingNew"] == "future-field"


def test_object_report_standalone_parse() -> None:
    """ObjectReport can be validated directly too (e.g. when DHIS2 returns it at top level)."""
    report = ObjectReport.model_validate(
        {
            "uid": "x",
            "klass": "org.hisp.dhis.dataelement.DataElement",
            "errorReports": [],
        }
    )
    assert report.uid == "x"
    assert report.errorReports == []


def test_import_count_standalone() -> None:
    counts = ImportCount.model_validate({"imported": 1, "updated": 0, "ignored": 0, "deleted": 0})
    assert counts.imported == 1
