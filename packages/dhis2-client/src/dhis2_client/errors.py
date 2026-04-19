"""Exception hierarchy for dhis2-client."""

from __future__ import annotations

from dhis2_client.envelopes import WebMessageResponse


class Dhis2ClientError(Exception):
    """Base class for all dhis2-client errors."""


class Dhis2ApiError(Dhis2ClientError):
    """Raised when the DHIS2 API returns a non-success response."""

    def __init__(self, status_code: int, message: str, body: object | None = None) -> None:
        """Capture HTTP status, message, and optional response body."""
        super().__init__(f"DHIS2 API returned {status_code}: {message}")
        self.status_code = status_code
        self.message = message
        self.body = body

    @property
    def web_message(self) -> WebMessageResponse | None:
        """Parse `body` as a WebMessageResponse when the shape matches, else None.

        DHIS2 returns the envelope on errors too (e.g. 409 on /api/dataValueSets
        with `status=WARNING` + populated `conflicts[]`), so callers can inspect
        import counts and per-row rejections without re-parsing.
        """
        if not isinstance(self.body, dict):
            return None
        try:
            return WebMessageResponse.model_validate(self.body)
        except Exception:
            return None


class AuthenticationError(Dhis2ClientError):
    """Raised when authentication fails or tokens are invalid."""


class OAuth2FlowError(Dhis2ClientError):
    """Raised when the OAuth 2.1 authorization-code flow fails."""


class UnsupportedVersionError(Dhis2ClientError):
    """Raised when the DHIS2 instance version has no generated client and fallback is disabled."""

    def __init__(self, version: str, available: list[str]) -> None:
        """Capture the reported version and the list of versions we have codegen for."""
        summary = ", ".join(available) if available else "none"
        super().__init__(
            f"DHIS2 instance reports version {version}; "
            f"no generated client available (have: {summary}). "
            "Run `dhis2 codegen --url <instance>` to generate one."
        )
        self.version = version
        self.available = available
