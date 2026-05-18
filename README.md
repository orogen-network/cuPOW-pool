# cuPOW-pool — PLACEHOLDER

**Status:** PLACEHOLDER. The real cuPOW share-aggregator / mining-pool service
is specified in [RFC-0008](../specs/rfc-0008-cupow.md) and has not yet been
implemented.

All endpoints on this service return **HTTP 503** with the body
`{"error": "cuPOW pool not yet implemented"}` **except** `GET /healthz`, which
returns HTTP 200 with `{"status": "stub", ...}` so a load-balancer can probe
the service without flapping.

This placeholder closes the silently-broken empty-directory state flagged in
[security-audit/03-workers.md](../security-audit/03-workers.md) as **C-06**.
If a downstream consumer (gateway, billing) mistakenly routes work-claims
here, it will fail loudly with 503 rather than silently accept the claim.

## Running

```bash
uv run uvicorn cupow_pool.app:app --port 8000
```

## Testing

```bash
uv run pytest
```

## When the real service lands

Replace `src/cupow_pool/app.py` with the actual share-aggregator implementation
and update this README. The placeholder package name (`cupow-pool`) and the
build layout should remain stable so downstream consumers do not need a
reconfiguration.
