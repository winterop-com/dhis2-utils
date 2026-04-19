"""FastAPI-backed OAuth2 redirect receiver.

Replaces `dhis2_client.auth.oauth2._capture_code`'s bare `asyncio.start_server`
implementation with a uvicorn-hosted FastAPI app. One GET handler captures the
redirect, validates state, and returns a styled HTML confirmation page.
"""

from __future__ import annotations

import asyncio
import urllib.parse
import webbrowser

import uvicorn
from dhis2_client.errors import OAuth2FlowError
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

_SUCCESS_HTML = """<!doctype html>
<html><head><meta charset="utf-8"><title>dhis2-utils login</title>
<style>
 body {{
   font-family: -apple-system, system-ui, sans-serif;
   padding: 3rem; color: #eee; background: #0f1117;
 }}
 .box {{
   max-width: 540px; margin: 0 auto; padding: 2rem;
   background: #1a1d26; border-radius: 12px;
   border: 1px solid #2a2e3a;
 }}
 h1 {{ margin: 0 0 0.5rem; color: #4ade80;
      font-weight: 500; font-size: 1.5rem; }}
 p {{ color: #a1a1aa; line-height: 1.5; }}
</style></head>
<body><div class="box">
 <h1>{heading}</h1>
 <p>{body}</p>
</div></body></html>
"""


async def capture_code(
    redirect_uri: str,
    expected_state: str,
    *,
    open_url: str | None = None,
    timeout: float = 300.0,
) -> str:
    """Open a uvicorn server at `redirect_uri` host:port, wait for the OAuth2 redirect, return `code`.

    If `open_url` is provided, the user's default browser is opened to that URL
    once the server is listening (the typical flow — we open the DHIS2
    authorize URL which then redirects back here).

    Raises `OAuth2FlowError` on state mismatch, provider-supplied error, or
    timeout. Shuts the server down on return.
    """
    parsed = urllib.parse.urlparse(redirect_uri)
    host = parsed.hostname or "localhost"
    port = parsed.port or 8765

    loop = asyncio.get_running_loop()
    captured: asyncio.Future[str] = loop.create_future()

    app = FastAPI()

    @app.get("/{_path:path}")
    async def _receive(request: Request, _path: str = "") -> HTMLResponse:
        params = request.query_params
        error = params.get("error")
        if error:
            description = params.get("error_description") or error
            if not captured.done():
                captured.set_exception(OAuth2FlowError(f"authorization failed: {description}"))
            return HTMLResponse(
                _SUCCESS_HTML.format(heading="Authentication failed", body=description),
                status_code=400,
            )
        state = params.get("state")
        if state != expected_state:
            if not captured.done():
                captured.set_exception(OAuth2FlowError("state mismatch — possible CSRF"))
            return HTMLResponse(
                _SUCCESS_HTML.format(heading="Authentication failed", body="State mismatch."),
                status_code=400,
            )
        code = params.get("code")
        if not code:
            if not captured.done():
                captured.set_exception(OAuth2FlowError("no authorization code returned"))
            return HTMLResponse(
                _SUCCESS_HTML.format(heading="Authentication failed", body="No authorization code in redirect."),
                status_code=400,
            )
        if not captured.done():
            captured.set_result(code)
        return HTMLResponse(
            _SUCCESS_HTML.format(
                heading="Authentication successful",
                body="You can close this tab and return to the terminal.",
            )
        )

    # ws="none" skips uvicorn's websocket protocol loading — we only need plain HTTP here,
    # and avoiding the import also silences a DeprecationWarning that uvicorn's legacy
    # websockets integration raises under `websockets>=14`.
    config = uvicorn.Config(app, host=host, port=port, log_level="error", access_log=False, ws="none")
    server = uvicorn.Server(config)
    serve_task = asyncio.create_task(server.serve())
    try:
        while not server.started:
            if serve_task.done():  # startup failed (e.g. port in use)
                serve_task.result()
                raise OAuth2FlowError(f"redirect server did not start on {host}:{port}")
            await asyncio.sleep(0.05)
        if open_url:
            webbrowser.open(open_url)
        return await asyncio.wait_for(captured, timeout=timeout)
    except TimeoutError as exc:
        raise OAuth2FlowError(f"no OAuth2 redirect received within {timeout}s") from exc
    finally:
        server.should_exit = True
        try:
            await asyncio.wait_for(serve_task, timeout=5.0)
        except TimeoutError:
            serve_task.cancel()
