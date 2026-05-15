"""v41 metadata targets `generated.v41` SharingObject + Literal-typed status field."""

from __future__ import annotations

import typing

from dhis2w_client.v41.envelopes import WebMessageResponse


def test_v41_metadata_sharing_object_comes_from_v41_generated_tree() -> None:
    """`v41.metadata.SharingObject` lives in the v41 generated tree."""
    import dhis2w_client.v41.metadata as metadata_module

    sharing_object = vars(metadata_module)["SharingObject"]
    assert sharing_object.__module__ == "dhis2w_client.generated.v41.oas.sharing_object"


def test_v41_web_message_response_status_is_literal() -> None:
    """v41 `WebMessageResponse.status` is `Literal["OK", "WARNING", "ERROR"] | None`."""
    annotation = WebMessageResponse.model_fields["status"].annotation
    union_args = typing.get_args(annotation)
    literal_member = next(arg for arg in union_args if arg is not type(None))
    assert set(typing.get_args(literal_member)) == {"OK", "WARNING", "ERROR"}
    assert type(None) in union_args
