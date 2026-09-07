from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint_returns_running_status() -> None:
    """
    The existing health endpoint remains available
    for general application health checks.
    """

    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "running"
    assert "service" in body
    assert "environment" in body
    assert "version" in body


def test_liveness_endpoint_returns_alive_status() -> None:
    """
    The liveness endpoint confirms that the application
    process is running.
    """

    with TestClient(app) as client:
        response = client.get("/health/live")

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "alive"
    assert "service" in body
    assert "environment" in body
    assert "version" in body


def test_readiness_endpoint_returns_ready_status() -> None:
    """
    The readiness endpoint confirms that the application
    can communicate with its database.
    """

    with TestClient(app) as client:
        response = client.get("/health/ready")

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "ready"
    assert body["database"] == "available"
    assert "service" in body
    assert "environment" in body
    assert "version" in body