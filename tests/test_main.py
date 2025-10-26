from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
def test_read_root(client: TestClient):
    """Test root endpoint returns proper response."""
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["message"] == "Skogsstyrelsen API Gateway"


@pytest.mark.unit
def test_health_check(client: TestClient):
    """Test health check endpoint."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data == {"status": "healthy"}


@pytest.mark.unit
def test_openapi_docs(client: TestClient):
    """Test OpenAPI documentation is available."""
    response = client.get("/docs")
    assert response.status_code == 200


@pytest.mark.unit
def test_openapi_json(client: TestClient):
    """Test OpenAPI JSON schema is available."""
    response = client.get("/openapi.json")

    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "paths" in data
    assert "info" in data


@pytest.mark.unit
def test_cors_headers(client: TestClient):
    """Test CORS headers are present."""
    response = client.options(
        "/api/grunddata/biomassa",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers


@pytest.mark.unit
def test_404_not_found(client: TestClient):
    """Test 404 response for non-existent endpoint."""
    response = client.get("/nonexistent")

    assert response.status_code == 404
