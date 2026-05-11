"""v41 files module targets `generated.v41` for Document + FileResource + FileResourceDomain."""

from __future__ import annotations


def test_v41_files_imports_from_v41_generated_tree() -> None:
    """`v41.files` wires its types from the v41 generated tree, not v42."""
    import dhis2w_client.v41.files as files_module

    assert files_module.Document.__module__ == "dhis2w_client.generated.v41.oas.document"
    assert files_module.FileResource.__module__ == "dhis2w_client.generated.v41.oas.file_resource"
    assert files_module.FileResourceDomain.__module__ == "dhis2w_client.generated.v41.enums"
