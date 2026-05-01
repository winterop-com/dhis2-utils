"""Async DHIS2 API client with pluggable auth and pydantic models.

The package exposes no top-level re-exports. Import directly from the
submodule that owns each symbol — e.g.

    from dhis2_client.client import Dhis2Client
    from dhis2_client.errors import Dhis2ApiError
    from dhis2_client.envelopes import WebMessageResponse

Direct imports keep startup time bounded (the package init does no work)
and make each module's dependency surface visible at the call site.
"""
