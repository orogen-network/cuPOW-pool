"""cuPOW-pool — placeholder package.

The real cuPOW share-aggregator service is specified in RFC-0008 but is not
yet implemented. This package ships a FastAPI app that returns 503 for every
endpoint except `/healthz`, which reports the stub status. The placeholder
exists so that downstream consumers (gateway, billing) fail loudly when they
mistakenly route work-claims to a not-yet-built service — closing the
silently-broken empty-dir state flagged in security-audit/03-workers.md
(C-06).
"""

from cupow_pool.app import build_app

__all__ = ["build_app"]
__version__ = "0.0.1"
