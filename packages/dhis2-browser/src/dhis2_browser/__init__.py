"""Playwright-based helpers for DHIS2 UI automation."""

from dhis2_browser.dashboard import (
    CaptureResult,
    DashboardTarget,
    add_banner,
    capture_dashboard,
    slugify,
    switch_dashboard,
    trim_background,
)
from dhis2_browser.pat import PatAttribute, PatOptions, PatPayload, create_pat
from dhis2_browser.session import logged_in_page, resolve_headless, session_from_cookie

__all__ = [
    "CaptureResult",
    "DashboardTarget",
    "PatAttribute",
    "PatOptions",
    "PatPayload",
    "add_banner",
    "capture_dashboard",
    "create_pat",
    "logged_in_page",
    "resolve_headless",
    "session_from_cookie",
    "slugify",
    "switch_dashboard",
    "trim_background",
]
