from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
def test_get_valid_projection_dates(client: TestClient):
    """Test GET /api/grunddata/valid-dates endpoint."""
    mock_response = ["2024-01-01", "2025-01-01", "2026-01-01"]

    with patch(
        "backend.services.skogsstyrelsen_client.SkogsstyrelsenClient.get",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        response = client.get("/api/grunddata/valid-dates")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3


@pytest.mark.unit
def test_get_biomassa(client: TestClient):
    """Test POST /api/grunddata/biomassa endpoint."""
    request_data = {
        "geometri": "POLYGON ((485486 7018193, 486179 7018193, 486179 7018896, 485486 7018896, 485486 7018193))",
        "marktyp": ["ProduktivSkogsmark"],
        "pixelstorlek": 2,
    }

    mock_response = {
        "data": {
            "ProduktivSkogsmark": {
                "arealHa": 50.0,
                "medelvarde": 120.5,
                "total": 6025.0,
            }
        },
        "metadataDto": {"pixelstorlek": 2, "omdrev": 2},
    }

    with patch(
        "backend.services.skogsstyrelsen_client.SkogsstyrelsenClient.post",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        response = client.post("/api/grunddata/biomassa", json=request_data)

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "ProduktivSkogsmark" in data["data"]


@pytest.mark.unit
def test_get_volym(client: TestClient):
    """Test POST /api/grunddata/volym endpoint."""
    request_data = {
        "geometri": "POLYGON ((485486 7018193, 486179 7018193, 486179 7018896, 485486 7018896, 485486 7018193))",
        "marktyp": ["ProduktivSkogsmark"],
    }

    mock_response = {
        "data": {
            "ProduktivSkogsmark": {
                "arealHa": 50.0,
                "medel": 180.5,
                "total": 9025.0,
            }
        }
    }

    with patch(
        "backend.services.skogsstyrelsen_client.SkogsstyrelsenClient.post",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        response = client.post("/api/grunddata/volym", json=request_data)

    assert response.status_code == 200
    data = response.json()
    assert "data" in data


@pytest.mark.unit
def test_get_biomassa_histogram(client: TestClient):
    """Test POST /api/grunddata/biomassa/histogram endpoint."""
    request_data = {
        "geometri": "POLYGON ((485486 7018193, 486179 7018193, 486179 7018896, 485486 7018896, 485486 7018193))",
        "marktyp": ["ProduktivSkogsmark"],
        "klassBredd": 100,
        "antalKlasser": 10,
    }

    mock_response = {
        "data": {
            "ProduktivSkogsmark": [
                {"klass": 1, "klassMinVarde": 0, "klassMaxVarde": 100, "arealHa": 10.5}
            ]
        },
        "klassbredd": 100,
        "pixelstorlek": 2,
    }

    with patch(
        "backend.services.skogsstyrelsen_client.SkogsstyrelsenClient.post",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        response = client.post("/api/grunddata/biomassa/histogram", json=request_data)

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "klassbredd" in data


@pytest.mark.unit
def test_get_grundyta(client: TestClient):
    """Test POST /api/grunddata/grundyta endpoint."""
    request_data = {
        "geometri": "POLYGON ((485486 7018193, 486179 7018193, 486179 7018896, 485486 7018896, 485486 7018193))",
        "marktyp": ["AllSkogsmark"],
    }

    mock_response = {
        "data": {"AllSkogsmark": {"arealHa": 100.0, "medel": 25.5}}
    }

    with patch(
        "backend.services.skogsstyrelsen_client.SkogsstyrelsenClient.post",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        response = client.post("/api/grunddata/grundyta", json=request_data)

    assert response.status_code == 200
    data = response.json()
    assert "data" in data


@pytest.mark.unit
def test_get_medelhojd(client: TestClient):
    """Test POST /api/grunddata/medelhojd endpoint."""
    request_data = {
        "geometri": "POLYGON ((485486 7018193, 486179 7018193, 486179 7018896, 485486 7018896, 485486 7018193))",
    }

    mock_response = {
        "data": {"ProduktivSkogsmark": {"arealHa": 50.0, "medelvarde": 18.5}}
    }

    with patch(
        "backend.services.skogsstyrelsen_client.SkogsstyrelsenClient.post",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        response = client.post("/api/grunddata/medelhojd", json=request_data)

    assert response.status_code == 200


@pytest.mark.unit
def test_get_medeldiameter(client: TestClient):
    """Test POST /api/grunddata/medeldiameter endpoint."""
    request_data = {
        "geometri": "POLYGON ((485486 7018193, 486179 7018193, 486179 7018896, 485486 7018896, 485486 7018193))",
    }

    mock_response = {
        "data": {"ProduktivSkogsmark": {"arealHa": 50.0, "medelvarde": 22.3}}
    }

    with patch(
        "backend.services.skogsstyrelsen_client.SkogsstyrelsenClient.post",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        response = client.post("/api/grunddata/medeldiameter", json=request_data)

    assert response.status_code == 200


@pytest.mark.unit
def test_get_volym_framskriven(client: TestClient):
    """Test POST /api/grunddata/volym-framskriven endpoint."""
    request_data = {
        "geometri": "POLYGON ((485486 7018193, 486179 7018193, 486179 7018896, 485486 7018896, 485486 7018193))",
        "datum": "2025-01-01",
    }

    mock_response = {
        "volym": {"ProduktivSkogsmark": {"arealHa": 50.0, "medel": 200.0}},
        "medelhojd": {"ProduktivSkogsmark": {"arealHa": 50.0, "medelvarde": 20.0}},
        "grundyta": {"ProduktivSkogsmark": {"arealHa": 50.0, "medel": 28.0}},
    }

    with patch(
        "backend.services.skogsstyrelsen_client.SkogsstyrelsenClient.post",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        response = client.post("/api/grunddata/volym-framskriven", json=request_data)

    assert response.status_code == 200
    data = response.json()
    assert "volym" in data
    assert "medelhojd" in data


@pytest.mark.unit
def test_grunddata_validation_error(client: TestClient):
    """Test validation error for invalid pixel size."""
    request_data = {
        "geometri": "POLYGON ((485486 7018193, 486179 7018193, 486179 7018896, 485486 7018896, 485486 7018193))",
        "pixelstorlek": 1,  # Below minimum of 2
    }

    response = client.post("/api/grunddata/biomassa", json=request_data)

    assert response.status_code == 422  # Validation error
