"""cuPOW-pool placeholder FastAPI app.

C-06 fix: previously this directory was empty, which silently led downstream
consumers (gateway, billing) to accept any work-claim because no validator
existed on the path. This module ships a refuse-to-serve placeholder so a
misrouted request fails closed with HTTP 503 rather than silently succeeding.

Endpoints:
- `GET  /healthz` — returns `{"status": "stub", ...}` with HTTP 200 so a
  load-balancer can probe the service without flapping.
- everything else — HTTP 503 with `{"error": "cuPOW pool not yet implemented"}`.

Once the real share-aggregator (RFC-0008) lands, replace this module wholesale.
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


def build_app() -> FastAPI:
    app = FastAPI(
        title="cuPOW-pool (PLACEHOLDER)",
        version="0.0.1",
        description=(
            "Placeholder service. The real cuPOW share-aggregator is "
            "specified in RFC-0008 and not yet implemented. Every endpoint "
            "except /healthz returns HTTP 503."
        ),
    )

    @app.get("/healthz")
    async def healthz() -> dict[str, Any]:
        return {
            "status": "stub",
            "service": "cuPOW-pool",
            "version": "0.0.1",
            "ready": False,
            "message": (
                "cuPOW pool not yet implemented; see RFC-0008. "
                "All non-healthz endpoints return HTTP 503."
            ),
        }

    # Catch-all that runs after FastAPI's own route table is empty. We attach
    # a generic exception handler-style middleware: any unmatched request gets
    # a 503. We use a catch-all route rather than middleware so /healthz above
    # still wins by virtue of being declared first.
    @app.api_route(
        "/{full_path:path}",
        methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"],
    )
    async def not_implemented(full_path: str, request: Request) -> JSONResponse:
        return JSONResponse(
            status_code=503,
            content={
                "error": "cuPOW pool not yet implemented",
                "path": "/" + full_path,
                "method": request.method,
                "rfc": "RFC-0008",
                "hint": "This service is a placeholder. Do not route work-claims here.",
            },
        )

    return app


app = build_app()
