"""v41 maintenance targets `generated.v41` + carries local NotificationDataType / NotificationLevel stubs."""

from __future__ import annotations

from dhis2w_client.v41.maintenance import (
    JobType,
    NotificationDataType,
    NotificationLevel,
)


def test_v41_maintenance_imports_from_v41_generated_tree() -> None:
    """DataIntegrityCheck, DataIntegrityIssue, Notification, and JobType come from generated.v41."""
    import dhis2w_client.v41.maintenance as maintenance_module

    assert maintenance_module.DataIntegrityCheck.__module__ == "dhis2w_client.generated.v41.oas.data_integrity_check"
    assert maintenance_module.DataIntegrityIssue.__module__ == "dhis2w_client.generated.v41.oas.data_integrity_issue"
    assert maintenance_module.Notification.__module__ == "dhis2w_client.generated.v41.oas.notification"
    assert JobType.__module__ == "dhis2w_client.generated.v41.enums"


def test_v41_notification_dataype_and_level_are_local_stubs() -> None:
    """v41 NotificationDataType / NotificationLevel are local StrEnum stubs (v41 OAS lacks them)."""
    assert NotificationDataType.__module__ == "dhis2w_client.v41.maintenance"
    assert NotificationLevel.__module__ == "dhis2w_client.v41.maintenance"
    assert NotificationDataType.PARAMETERS.value == "PARAMETERS"
    assert {member.value for member in NotificationLevel} == {"OFF", "DEBUG", "LOOP", "INFO", "WARN", "ERROR"}
