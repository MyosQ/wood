from __future__ import annotations

import pytest

from backend.core.exceptions import (
    APIError,
    AuthenticationError,
    ConfigurationError,
    SkogsstyrelsenError,
)


@pytest.mark.unit
def test_base_exception():
    """Test base SkogsstyrelsenError."""
    error = SkogsstyrelsenError("Test error", status_code=500)

    assert str(error) == "Test error"
    assert error.message == "Test error"
    assert error.status_code == 500


@pytest.mark.unit
def test_authentication_error():
    """Test AuthenticationError defaults."""
    error = AuthenticationError()

    assert "Authentication failed" in str(error)
    assert error.status_code == 401


@pytest.mark.unit
def test_authentication_error_custom_message():
    """Test AuthenticationError with custom message."""
    error = AuthenticationError("Invalid token")

    assert str(error) == "Invalid token"
    assert error.status_code == 401


@pytest.mark.unit
def test_api_error():
    """Test APIError."""
    error = APIError("API failed", status_code=502)

    assert str(error) == "API failed"
    assert error.status_code == 502


@pytest.mark.unit
def test_configuration_error():
    """Test ConfigurationError defaults."""
    error = ConfigurationError()

    assert "Configuration error" in str(error)
    assert error.status_code == 500


@pytest.mark.unit
def test_exception_inheritance():
    """Test exception inheritance hierarchy."""
    assert issubclass(AuthenticationError, SkogsstyrelsenError)
    assert issubclass(APIError, SkogsstyrelsenError)
    assert issubclass(ConfigurationError, SkogsstyrelsenError)
