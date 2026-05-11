"""v43 sharing divergence — `externalAccess` was dropped from `SharingObject`.

The v43 server schema removed the `externalAccess` field entirely, so the
v43 `SharingBuilder` doesn't expose `external_access` and the materialised
`SharingObject` does not emit the key. The v42 sibling at
`dhis2w_client.v42.sharing` still carries both — verified separately.
"""

from __future__ import annotations


def test_v43_sharing_builder_drops_external_access_field() -> None:
    """The v43 SharingBuilder no longer declares `external_access` as a field."""
    from dhis2w_client.v43.sharing import SharingBuilder

    assert "external_access" not in SharingBuilder.model_fields


def test_v43_to_sharing_object_does_not_emit_external_access() -> None:
    """The materialised v43 SharingObject wire shape omits `externalAccess`."""
    from dhis2w_client.v43.sharing import ACCESS_READ_METADATA, SharingBuilder

    builder = SharingBuilder(public_access=ACCESS_READ_METADATA)
    sharing_object = builder.to_sharing_object()
    dumped = sharing_object.model_dump(by_alias=True, exclude_none=True)
    assert "externalAccess" not in dumped


def test_v42_sharing_builder_keeps_external_access_field() -> None:
    """The v42 SharingBuilder still carries `external_access` (sanity check on the sibling)."""
    from dhis2w_client.v42.sharing import SharingBuilder as V42Builder

    assert "external_access" in V42Builder.model_fields
