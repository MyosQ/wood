from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient


def mock_get_api_client():
    """Mock dependency for get_api_client."""
    mock_client = MagicMock()
    mock_client.get = AsyncMock()
    mock_client.post = AsyncMock()
    return mock_client


@pytest.mark.unit
def test_get_raster_api_info(client: TestClient):
    """Test GET /api/raster/api-info endpoint."""
    from backend.core.dependencies import get_api_client
    from backend.main import app

    mock_response = {
        "apiName": "Raster API",
        "apiVersion": "1.0",
        "apiReleased": "2024-01-01",
        "apiDocumentation": "https://example.com",
        "apiStatus": "active",
    }

    mock_client = mock_get_api_client()
    mock_client.get.return_value = mock_response

    app.dependency_overrides[get_api_client] = lambda: mock_client

    try:
        response = client.get("/api/raster/api-info")
        assert response.status_code == 200
        data = response.json()
        assert "apiName" in data
        assert data["apiName"] == "Raster API"
    finally:
        app.dependency_overrides.clear()


@pytest.mark.unit
def test_scl_histogram_date_summary(client: TestClient):
    """Test POST /api/raster/scl/histogram-date-summary endpoint."""
    request_data = {
        "minDatum": "2023-01-01",
        "maxDatum": "2023-12-31",
        "extent": "POLYGON ((485486 7018193, 486179 7018193, 486179 7018896, 485486 7018896, 485486 7018193))",
    }

    mock_response = {"dates": [{"datum": "2023-06-01", "braData": 0.95}]}

    with patch(
        "backend.services.skogsstyrelsen_client.SkogsstyrelsenClient.post",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        response = client.post("/api/raster/scl/histogram-date-summary", json=request_data)

    assert response.status_code == 200
    data = response.json()
    assert "dates" in data


@pytest.mark.unit
def test_scl_histogram_by_bkid(client: TestClient):
    """Test POST /api/raster/scl/histogram-by-bkid endpoint."""
    request_data = {
        "minDatum": "2023-01-01",
        "maxDatum": "2023-12-31",
        "bkId": "701_48_50",
    }

    mock_response = {"histogram": [{"class": 1, "count": 100}]}

    with patch(
        "backend.services.skogsstyrelsen_client.SkogsstyrelsenClient.post",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        response = client.post("/api/raster/scl/histogram-by-bkid", json=request_data)

    assert response.status_code == 200
    data = response.json()
    assert "histogram" in data


@pytest.mark.unit
def test_scl_histogram_date_summary_validation_error(client: TestClient):
    """Test validation error for missing required fields."""
    request_data = {
        "minDatum": "2023-01-01",
        # Missing required 'extent' field
    }

    response = client.post("/api/raster/scl/histogram-date-summary", json=request_data)

    assert response.status_code == 422  # Validation error
    data = response.json()
    assert "detail" in data
