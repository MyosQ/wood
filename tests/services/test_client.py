from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from backend.core.config import Settings
from backend.core.exceptions import APIError
from backend.services.auth import SkogsstyrelsenAuth
from backend.services.skogsstyrelsen_client import SkogsstyrelsenClient


@pytest.mark.unit
async def test_client_get_request(
    mock_auth: SkogsstyrelsenAuth, test_settings: Settings
):
    """Test client makes GET request properly."""
    client = SkogsstyrelsenClient(mock_auth, test_settings)

    mock_response = MagicMock()
    mock_response.json.return_value = {"data": "test"}
    mock_response.raise_for_status = MagicMock()

    mock_http_client = MagicMock()
    mock_http_client.request = AsyncMock(return_value=mock_response)
    mock_http_client.is_closed = False

    with patch.object(client, "_get_client", return_value=mock_http_client):
        result = await client.get("/test/endpoint")

    assert result == {"data": "test"}
    mock_auth.get_token.assert_called_once()


@pytest.mark.unit
async def test_client_post_request(
    mock_auth: SkogsstyrelsenAuth, test_settings: Settings
):
    """Test client makes POST request properly."""
    client = SkogsstyrelsenClient(mock_auth, test_settings)

    mock_response = MagicMock()
    mock_response.json.return_value = {"success": True}
    mock_response.raise_for_status = MagicMock()

    mock_http_client = MagicMock()
    mock_http_client.request = AsyncMock(return_value=mock_response)
    mock_http_client.is_closed = False

    with patch.object(client, "_get_client", return_value=mock_http_client):
        result = await client.post("/test/endpoint", {"key": "value"})

    assert result == {"success": True}


@pytest.mark.unit
async def test_client_handles_http_error(
    mock_auth: SkogsstyrelsenAuth, test_settings: Settings
):
    """Test client handles HTTP errors properly."""
    client = SkogsstyrelsenClient(mock_auth, test_settings)

    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "Bad request"

    mock_http_client = MagicMock()
    mock_http_client.request = AsyncMock(
        side_effect=httpx.HTTPStatusError(
            "Error", request=MagicMock(), response=mock_response
        )
    )
    mock_http_client.is_closed = False

    with patch.object(client, "_get_client", return_value=mock_http_client):
        with pytest.raises(APIError) as exc_info:
            await client.get("/test/endpoint")

        assert "API request failed" in str(exc_info.value)
        assert exc_info.value.status_code == 400


@pytest.mark.unit
async def test_client_handles_network_error(
    mock_auth: SkogsstyrelsenAuth, test_settings: Settings
):
    """Test client handles network errors properly."""
    client = SkogsstyrelsenClient(mock_auth, test_settings)

    mock_http_client = MagicMock()
    mock_http_client.request = AsyncMock(
        side_effect=httpx.RequestError("Connection failed")
    )
    mock_http_client.is_closed = False

    with patch.object(client, "_get_client", return_value=mock_http_client):
        with pytest.raises(APIError) as exc_info:
            await client.get("/test/endpoint")

        assert "Request failed" in str(exc_info.value)


@pytest.mark.unit
async def test_client_constructs_url_correctly(
    mock_auth: SkogsstyrelsenAuth, test_settings: Settings
):
    """Test client constructs full URL correctly."""
    client = SkogsstyrelsenClient(mock_auth, test_settings)

    mock_response = MagicMock()
    mock_response.json.return_value = {}
    mock_response.raise_for_status = MagicMock()

    mock_http_client = MagicMock()
    mock_request = AsyncMock(return_value=mock_response)
    mock_http_client.request = mock_request
    mock_http_client.is_closed = False

    with patch.object(client, "_get_client", return_value=mock_http_client):
        await client.get("/test/endpoint")

        # Check URL construction
        call_kwargs = mock_request.call_args[1]
        assert call_kwargs["url"] == f"{test_settings.skogsstyrelsen_base_url}/test/endpoint"


@pytest.mark.unit
async def test_client_includes_auth_header(
    mock_auth: SkogsstyrelsenAuth, test_settings: Settings
):
    """Test client includes authorization header."""
    client = SkogsstyrelsenClient(mock_auth, test_settings)

    mock_response = MagicMock()
    mock_response.json.return_value = {}
    mock_response.raise_for_status = MagicMock()

    mock_http_client = MagicMock()
    mock_request = AsyncMock(return_value=mock_response)
    mock_http_client.request = mock_request
    mock_http_client.is_closed = False

    with patch.object(client, "_get_client", return_value=mock_http_client):
        await client.get("/test/endpoint")

        # Check auth header
        call_kwargs = mock_request.call_args[1]
        assert "Authorization" in call_kwargs["headers"]
        assert call_kwargs["headers"]["Authorization"] == "Bearer mock_access_token"


@pytest.mark.unit
async def test_client_passes_params_correctly(
    mock_auth: SkogsstyrelsenAuth, test_settings: Settings
):
    """Test client passes query parameters correctly."""
    client = SkogsstyrelsenClient(mock_auth, test_settings)

    mock_response = MagicMock()
    mock_response.json.return_value = {}
    mock_response.raise_for_status = MagicMock()

    mock_http_client = MagicMock()
    mock_request = AsyncMock(return_value=mock_response)
    mock_http_client.request = mock_request
    mock_http_client.is_closed = False

    with patch.object(client, "_get_client", return_value=mock_http_client):
        await client.get("/test/endpoint", params={"key": "value"})

        call_kwargs = mock_request.call_args[1]
        assert call_kwargs["params"] == {"key": "value"}


@pytest.mark.unit
async def test_client_passes_json_correctly(
    mock_auth: SkogsstyrelsenAuth, test_settings: Settings
):
    """Test client passes JSON data correctly."""
    client = SkogsstyrelsenClient(mock_auth, test_settings)

    mock_response = MagicMock()
    mock_response.json.return_value = {}
    mock_response.raise_for_status = MagicMock()

    mock_http_client = MagicMock()
    mock_request = AsyncMock(return_value=mock_response)
    mock_http_client.request = mock_request
    mock_http_client.is_closed = False

    with patch.object(client, "_get_client", return_value=mock_http_client):
        await client.post("/test/endpoint", {"test": "data"})

        call_kwargs = mock_request.call_args[1]
        assert call_kwargs["json"] == {"test": "data"}
