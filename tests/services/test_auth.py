from __future__ import annotations

from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from backend.core.config import Settings
from backend.core.exceptions import AuthenticationError
from backend.services.auth import SkogsstyrelsenAuth


@pytest.mark.unit
def test_auth_init_success(test_settings: Settings):
    """Test auth service initialization with valid credentials."""
    auth = SkogsstyrelsenAuth(test_settings)
    assert auth.settings == test_settings
    assert auth._access_token is None
    assert auth._token_expiry is None


@pytest.mark.unit
def test_auth_init_missing_credentials():
    """Test auth service initialization fails with missing credentials."""
    settings = Settings(
        skogsstyrelsen_client_id="",
        skogsstyrelsen_client_secret="test_secret",
    )

    with pytest.raises(AuthenticationError) as exc_info:
        SkogsstyrelsenAuth(settings)

    assert "must be set" in str(exc_info.value)


@pytest.mark.unit
async def test_get_token_fetches_new_token(test_settings: Settings):
    """Test get_token fetches new token when none exists."""
    auth = SkogsstyrelsenAuth(test_settings)

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "access_token": "new_token_123",
        "expires_in": 3600,
    }
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response
        )

        token = await auth.get_token()

    assert token == "new_token_123"
    assert auth._access_token == "new_token_123"
    assert auth._token_expiry is not None


@pytest.mark.unit
async def test_get_token_returns_cached_token(test_settings: Settings):
    """Test get_token returns cached token if still valid."""
    auth = SkogsstyrelsenAuth(test_settings)
    auth._access_token = "cached_token"
    auth._token_expiry = datetime.now() + timedelta(minutes=30)

    # Should not make HTTP request
    token = await auth.get_token()

    assert token == "cached_token"


@pytest.mark.unit
async def test_get_token_refreshes_expired_token(test_settings: Settings):
    """Test get_token refreshes token when expired."""
    auth = SkogsstyrelsenAuth(test_settings)
    auth._access_token = "old_token"
    auth._token_expiry = datetime.now() - timedelta(minutes=1)  # Expired

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "access_token": "refreshed_token",
        "expires_in": 3600,
    }
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response
        )

        token = await auth.get_token()

    assert token == "refreshed_token"


@pytest.mark.unit
async def test_get_token_handles_http_error(test_settings: Settings):
    """Test get_token handles HTTP errors properly."""
    auth = SkogsstyrelsenAuth(test_settings)

    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.text = "Invalid credentials"

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            side_effect=httpx.HTTPStatusError(
                "Auth failed", request=MagicMock(), response=mock_response
            )
        )

        with pytest.raises(AuthenticationError) as exc_info:
            await auth.get_token()

        assert "Failed to obtain token" in str(exc_info.value)


@pytest.mark.unit
async def test_get_token_handles_network_error(test_settings: Settings):
    """Test get_token handles network errors properly."""
    auth = SkogsstyrelsenAuth(test_settings)

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            side_effect=httpx.RequestError("Network error")
        )

        with pytest.raises(AuthenticationError) as exc_info:
            await auth.get_token()

        assert "Authentication request failed" in str(exc_info.value)


@pytest.mark.unit
def test_get_auth_header(test_settings: Settings):
    """Test get_auth_header returns proper format."""
    auth = SkogsstyrelsenAuth(test_settings)
    header = auth.get_auth_header("test_token_123")

    assert header == {"Authorization": "Bearer test_token_123"}


@pytest.mark.unit
def test_is_token_valid_no_token(test_settings: Settings):
    """Test _is_token_valid returns False when no token exists."""
    auth = SkogsstyrelsenAuth(test_settings)
    assert auth._is_token_valid() is False


@pytest.mark.unit
def test_is_token_valid_expired(test_settings: Settings):
    """Test _is_token_valid returns False when token is expired."""
    auth = SkogsstyrelsenAuth(test_settings)
    auth._access_token = "token"
    auth._token_expiry = datetime.now() - timedelta(minutes=1)

    assert auth._is_token_valid() is False


@pytest.mark.unit
def test_is_token_valid_near_expiry(test_settings: Settings):
    """Test _is_token_valid returns False when token expires within 5 minutes."""
    auth = SkogsstyrelsenAuth(test_settings)
    auth._access_token = "token"
    auth._token_expiry = datetime.now() + timedelta(minutes=3)  # Within 5 min buffer

    assert auth._is_token_valid() is False


@pytest.mark.unit
def test_is_token_valid_success(test_settings: Settings):
    """Test _is_token_valid returns True when token is valid."""
    auth = SkogsstyrelsenAuth(test_settings)
    auth._access_token = "token"
    auth._token_expiry = datetime.now() + timedelta(minutes=30)

    assert auth._is_token_valid() is True
