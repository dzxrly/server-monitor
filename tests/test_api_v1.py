from __future__ import annotations

from flask import Flask


def test_metrics_returns_one_coherent_snapshot(app: Flask) -> None:
    response = app.test_client().get("/api/v1/metrics?processLimit=2")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["apiVersion"] == "v1"
    assert payload["sequence"] >= 1
    assert payload["processes"]["limit"] == 2
    assert len(payload["processes"]["cpu"]) <= 2
    assert len(payload["processes"]["memory"]) <= 2
    assert len(payload["processes"]["gpu"]) <= 2
    assert {
        "system",
        "cpu",
        "memory",
        "gpu",
        "storage",
        "network",
        "processes",
        "capabilities",
    } <= payload.keys()


def test_metrics_uses_configured_default_process_limit(app: Flask) -> None:
    response = app.test_client().get("/api/v1/metrics")
    assert response.status_code == 200
    assert response.get_json()["processes"]["limit"] == 3


def test_metrics_rejects_invalid_process_limits(app: Flask) -> None:
    client = app.test_client()
    for value in ("0", "11", "not-a-number"):
        response = client.get(f"/api/v1/metrics?processLimit={value}")
        assert response.status_code == 400
        assert "processLimit" in response.get_json()["error"]


def test_health_and_capabilities_are_versioned(app: Flask) -> None:
    client = app.test_client()
    health = client.get("/api/v1/health")
    capabilities = client.get("/api/v1/capabilities")

    assert health.status_code == 200
    assert health.get_json() == {
        "apiVersion": "v1",
        "samplerRunning": True,
        "status": "ok",
    }
    assert capabilities.status_code == 200
    assert capabilities.get_json()["apiVersion"] == "v1"


def test_legacy_routes_are_removed(app: Flask) -> None:
    client = app.test_client()
    for route in (
        "/cpu_state",
        "/memory_state",
        "/gpu_state",
        "/network_state",
        "/operating_system",
    ):
        assert client.get(route).status_code == 404
