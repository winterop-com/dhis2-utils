"""DHIS2 v42 hand-written client surface.

Canonical implementation today — `Dhis2Client.connect()` auto-detects
the server version and loads from the matching `generated.v{N}` tree at
runtime. v41 / v43 sibling subpackages start as mechanical copies of
this tree and diverge as version-specific behaviour lands.
"""
