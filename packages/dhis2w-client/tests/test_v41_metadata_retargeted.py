"""v41 metadata targets `generated.v41` SharingObject + local Status stub."""

from __future__ import annotations

from dhis2w_client.v41.metadata import Status


def test_v41_metadata_sharing_object_comes_from_v41_generated_tree() -> None:
    """`v41.metadata.SharingObject` lives in the v41 generated tree."""
    import dhis2w_client.v41.metadata as metadata_module

    # `SharingObject` is imported by the module but not re-exported through
    # `__all__` — fetch via the module dict to avoid pyright's `reportPrivateImportUsage`.
    sharing_object = vars(metadata_module)["SharingObject"]
    assert sharing_object.__module__ == "dhis2w_client.generated.v41.oas.sharing_object"


def test_v41_status_is_local_stub() -> None:
    """v41 Status is a local StrEnum stub (v41 OAS lacks it)."""
    assert Status.__module__ == "dhis2w_client.v41.metadata"
    assert {member.value for member in Status} == {"OK", "WARNING", "ERROR"}
    assert Status.OK.value == "OK"
