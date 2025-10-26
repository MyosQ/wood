from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient


def mock_get_api_client():
    """Mock dependency for get_api_client."""
    from unittest.mock import AsyncMock, MagicMock

    mock_client = MagicMock()
    mock_client.get = AsyncMock()
    mock_client.post = AsyncMock()
    return mock_client


@pytest.mark.unit
def test_get_helalandet(client: TestClient):
    """Test GET /api/abin/helalandet endpoint."""
    mock_response = {
        "omrade": "Hela landet",
        "inventeringsAr": 2023,
        "lankod": None,
    }

    with patch(
        "backend.services.skogsstyrelsen_client.SkogsstyrelsenClient.get",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        response = client.get("/api/abin/helalandet")

    assert response.status_code == 200
    data = response.json()
    assert data["omrade"] == "Hela landet"


@pytest.mark.unit
def test_get_helalandet_geometri(client: TestClient):
    """Test GET /api/abin/helalandet/geometri endpoint."""
    mock_response = {
        "omrade": "Hela landet",
        "inventeringsAr": 2023,
        "geometri": "MULTIPOLYGON(...)",
    }

    with patch(
        "backend.services.skogsstyrelsen_client.SkogsstyrelsenClient.get",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        response = client.get("/api/abin/helalandet/geometri")

    assert response.status_code == 200
    data = response.json()
    assert "geometri" in data


@pytest.mark.unit
def test_get_landsdel_metadata(client: TestClient):
    """Test GET /api/abin/landsdel/metadata endpoint."""
    from backend.core.dependencies import get_api_client
    from backend.main import app

    mock_response = [
        {"landsdelkod": "1", "landsdelnamn": "Norra"},
        {"landsdelkod": "2", "landsdelnamn": "Södra"},
    ]

    mock_client = mock_get_api_client()
    mock_client.get.return_value = mock_response

    app.dependency_overrides[get_api_client] = lambda: mock_client

    try:
        response = client.get("/api/abin/landsdel/metadata")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
    finally:
        app.dependency_overrides.clear()


@pytest.mark.unit
def test_get_landsdel(client: TestClient):
    """Test GET /api/abin/landsdel/{landsdelkod} endpoint."""
    mock_response = {
        "omrade": "Norra Sverige",
        "landsdelkod": "1",
        "inventeringsAr": 2023,
    }

    with patch(
        "backend.services.skogsstyrelsen_client.SkogsstyrelsenClient.get",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        response = client.get("/api/abin/landsdel/1")

    assert response.status_code == 200
    data = response.json()
    assert data["landsdelkod"] == "1"


@pytest.mark.unit
def test_get_lan(client: TestClient):
    """Test GET /api/abin/lan/{lankod} endpoint."""
    mock_response = {
        "omrade": "Stockholm",
        "lankod": "01",
        "inventeringsAr": 2023,
    }

    with patch(
        "backend.services.skogsstyrelsen_client.SkogsstyrelsenClient.get",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        response = client.get("/api/abin/lan/01")

    assert response.status_code == 200
    data = response.json()
    assert data["lankod"] == "01"
    assert data["omrade"] == "Stockholm"


@pytest.mark.unit
def test_get_lan_geometri(client: TestClient):
    """Test GET /api/abin/lan/{lankod}/geometri endpoint."""
    mock_response = {
        "omrade": "Stockholm",
        "lankod": "01",
        "geometri": "MULTIPOLYGON(...)",
    }

    with patch(
        "backend.services.skogsstyrelsen_client.SkogsstyrelsenClient.get",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        response = client.get("/api/abin/lan/01/geometri")

    assert response.status_code == 200
    data = response.json()
    assert "geometri" in data


@pytest.mark.unit
def test_get_lan_metadata(client: TestClient):
    """Test GET /api/abin/landsdel/{landsdelkod}/lan/metadata endpoint."""
    from backend.core.dependencies import get_api_client
    from backend.main import app

    mock_response = [
        {"lankod": "01", "lannamn": "Stockholm"},
        {"lankod": "03", "lannamn": "Uppsala"},
    ]

    mock_client = mock_get_api_client()
    mock_client.get.return_value = mock_response

    app.dependency_overrides[get_api_client] = lambda: mock_client

    try:
        response = client.get("/api/abin/landsdel/2/lan/metadata")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    finally:
        app.dependency_overrides.clear()


@pytest.mark.unit
def test_get_afo(client: TestClient):
    """Test GET /api/abin/lan/{lankod}/afo/{afonr} endpoint."""
    mock_response = {
        "omrade": "ÄFO 101",
        "lankod": "01",
        "afonr": 101,
        "inventeringsAr": 2023,
    }

    with patch(
        "backend.services.skogsstyrelsen_client.SkogsstyrelsenClient.get",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        response = client.get("/api/abin/lan/01/afo/101")

    assert response.status_code == 200
    data = response.json()
    assert data["afonr"] == 101


@pytest.mark.unit
def test_get_afo_geometri(client: TestClient):
    """Test GET /api/abin/lan/{lankod}/afo/{afonr}/geometri endpoint."""
    mock_response = {
        "omrade": "ÄFO 101",
        "geometri": "MULTIPOLYGON(...)",
    }

    with patch(
        "backend.services.skogsstyrelsen_client.SkogsstyrelsenClient.get",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        response = client.get("/api/abin/lan/01/afo/101/geometri")

    assert response.status_code == 200
    data = response.json()
    assert "geometri" in data


@pytest.mark.unit
def test_get_afo_metadata(client: TestClient):
    """Test GET /api/abin/landsdel/{landsdelkod}/lan/{lankod}/afo/metadata endpoint."""
    from backend.core.dependencies import get_api_client
    from backend.main import app

    mock_response = [
        {"afonr": 101, "afonamn": "ÄFO 101"},
        {"afonr": 102, "afonamn": "ÄFO 102"},
    ]

    mock_client = mock_get_api_client()
    mock_client.get.return_value = mock_response

    app.dependency_overrides[get_api_client] = lambda: mock_client

    try:
        response = client.get("/api/abin/landsdel/2/lan/01/afo/metadata")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    finally:
        app.dependency_overrides.clear()


@pytest.mark.unit
def test_get_stratum(client: TestClient):
    """Test GET /api/abin/lan/{lankod}/afo/{afonr}/stratum/{delomradesnummer} endpoint."""
    mock_response = {
        "omrade": "Stratum 1",
        "delomradesnummer": 1,
        "inventeringsAr": 2023,
    }

    with patch(
        "backend.services.skogsstyrelsen_client.SkogsstyrelsenClient.get",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        response = client.get("/api/abin/lan/01/afo/101/stratum/1")

    assert response.status_code == 200
    data = response.json()
    assert data["delomradesnummer"] == 1


@pytest.mark.unit
def test_get_stratum_geometri(client: TestClient):
    """Test GET /api/abin/lan/{lankod}/afo/{afonr}/stratum/{delomradesnummer}/geometri endpoint."""
    mock_response = {
        "omrade": "Stratum 1",
        "geometri": "MULTIPOLYGON(...)",
    }

    with patch(
        "backend.services.skogsstyrelsen_client.SkogsstyrelsenClient.get",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        response = client.get("/api/abin/lan/01/afo/101/stratum/1/geometri")

    assert response.status_code == 200
    data = response.json()
    assert "geometri" in data


@pytest.mark.unit
def test_get_stratum_metadata(client: TestClient):
    """Test GET /api/abin/landsdel/{landsdelkod}/lan/{lankod}/afo/{afonr}/stratum/metadata endpoint."""
    from backend.core.dependencies import get_api_client
    from backend.main import app

    mock_response = [
        {"delomradesnummer": 1},
        {"delomradesnummer": 2},
    ]

    mock_client = mock_get_api_client()
    mock_client.get.return_value = mock_response

    app.dependency_overrides[get_api_client] = lambda: mock_client

    try:
        response = client.get("/api/abin/landsdel/2/lan/01/afo/101/stratum/metadata")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    finally:
        app.dependency_overrides.clear()


@pytest.mark.unit
def test_get_abin_api_info(client: TestClient):
    """Test GET /api/abin/api-info endpoint."""
    mock_response = {
        "apiName": "ABIN API",
        "apiVersion": "2.0",
        "apiStatus": "active",
    }

    with patch(
        "backend.services.skogsstyrelsen_client.SkogsstyrelsenClient.get",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        response = client.get("/api/abin/api-info")

    assert response.status_code == 200
    data = response.json()
    assert "apiName" in data
