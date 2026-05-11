"""v41 apps targets `generated.v41` with a local App subclass + AppStatus/AppType stubs."""

from __future__ import annotations

from dhis2w_client.v41.apps import App, AppStatus, AppType


def test_v41_app_is_subclass_of_v41_generated_app() -> None:
    """v41 App is a local subclass of the v41 generated App, adding `displayName`."""
    from dhis2w_client.generated.v41.oas import App as GeneratedV41App

    assert issubclass(App, GeneratedV41App)
    assert App.__module__ == "dhis2w_client.v41.apps"
    assert "displayName" in App.model_fields


def test_v41_app_declares_display_name_as_field() -> None:
    """`displayName` is a declared model field (not a forwarded extra)."""
    field_info = App.model_fields["displayName"]
    assert field_info.annotation == (str | None)
    assert field_info.default is None


def test_v41_app_status_and_type_are_local_stubs_with_full_value_set() -> None:
    """v41 AppStatus + AppType are local stubs whose values match v42 + v43's generated enums."""
    assert AppStatus.__module__ == "dhis2w_client.v41.apps"
    assert AppType.__module__ == "dhis2w_client.v41.apps"
    assert AppStatus.OK.value == "OK"
    assert AppType.DASHBOARD_WIDGET.value == "DASHBOARD_WIDGET"
    assert {member.value for member in AppType} == {"APP", "RESOURCE", "DASHBOARD_WIDGET"}
