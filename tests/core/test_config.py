from __future__ import annotations

import pytest

from backend.core.config import Settings, get_settings


@pytest.mark.unit
def test_settings_with_defaults():
    """Test settings initialization with default values."""
    settings = Settings(
        skogsstyrelsen_client_id="test_id",
        skogsstyrelsen_client_secret="test_secret",
    )

    assert settings.skogsstyrelsen_client_id == "test_id"
    assert settings.skogsstyrelsen_client_secret == "test_secret"
    assert settings.skogsstyrelsen_base_url == "https://api.skogsstyrelsen.se/sksapi"
    assert settings.app_title == "Skogsstyrelsen API Gateway"
    assert settings.debug is False
    assert settings.request_timeout == 30.0


@pytest.mark.unit
def test_settings_with_custom_values():
    """Test settings initialization with custom values."""
    settings = Settings(
        skogsstyrelsen_client_id="custom_id",
        skogsstyrelsen_client_secret="custom_secret",
        debug=True,
        request_timeout=60.0,
    )

    assert settings.debug is True
    assert settings.request_timeout == 60.0


@pytest.mark.unit
def test_settings_cors_origins():
    """Test CORS origins configuration."""
    settings = Settings(
        skogsstyrelsen_client_id="test",
        skogsstyrelsen_client_secret="test",
    )

    assert isinstance(settings.cors_origins, list)
    assert "http://localhost:5173" in settings.cors_origins


@pytest.mark.unit
def test_get_settings_is_cached():
    """Test that get_settings returns cached instance."""
    settings1 = get_settings()
    settings2 = get_settings()

    # Should be the exact same object due to lru_cache
    assert settings1 is settings2
