"""v41 messaging module targets `generated.v41` for MessageConversation + the two enums."""

from __future__ import annotations


def test_v41_messaging_imports_from_v41_generated_tree() -> None:
    """`v41.messaging` wires its types from the v41 generated tree, not v42."""
    import dhis2w_client.v41.messaging as messaging_module

    assert messaging_module.MessageConversation.__module__ == "dhis2w_client.generated.v41.oas.message_conversation"
    # `MessageConversationPriority` / `MessageConversationStatus` are imported by the
    # module but not re-exported through `__all__` — fetch via the module dict to
    # avoid pyright's `reportPrivateImportUsage`.
    module_attrs = vars(messaging_module)
    assert module_attrs["MessageConversationPriority"].__module__ == "dhis2w_client.generated.v41.enums"
    assert module_attrs["MessageConversationStatus"].__module__ == "dhis2w_client.generated.v41.enums"
