"""cuPOW-pool placeholder smoke tests.

Verifies that the placeholder service returns the expected stub status on
`/healthz` and rejects every other request with HTTP 503. See
security-audit/03-workers.md C-06 for context.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from cupow_pool import build_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(build_app())


def test_healthz_returns_stub(client: TestClient) -> None:
    r = client.get("/healthz")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "stub"
    assert body["ready"] is False
    assert body["service"] == "cuPOW-pool"


def test_unknown_get_route_returns_503(client: TestClient) -> None:
    r = client.get("/submit_share")
    assert r.status_code == 503
    body = r.json()
    assert body["error"] == "cuPOW pool not yet implemented"
    assert body["method"] == "GET"
    assert body["path"] == "/submit_share"


def test_unknown_post_route_returns_503(client: TestClient) -> None:
    r = client.post("/submit_share", json={"nonce": "0xdead"})
    assert r.status_code == 503
    body = r.json()
    assert body["error"] == "cuPOW pool not yet implemented"
    assert body["method"] == "POST"


def test_root_returns_503(client: TestClient) -> None:
    r = client.get("/")
    assert r.status_code == 503
    body = r.json()
    assert body["error"] == "cuPOW pool not yet implemented"


def test_put_delete_patch_all_503(client: TestClient) -> None:
    for method in ("PUT", "DELETE", "PATCH"):
        r = client.request(method, "/whatever")
        assert r.status_code == 503, f"{method} should 503, got {r.status_code}"
