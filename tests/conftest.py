from __future__ import annotations

import os
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from backend.core.config import Settings
from backend.main import app
from backend.services.auth import SkogsstyrelsenAuth
from backend.services.skogsstyrelsen_client import SkogsstyrelsenClient


@pytest.fixture
def test_settings() -> Settings:
    """Create test settings with mock credentials."""
    return Settings(
        skogsstyrelsen_client_id="test_client_id",
        skogsstyrelsen_client_secret="test_client_secret",
        debug=True,
    )


@pytest.fixture
def mock_auth(test_settings: Settings) -> SkogsstyrelsenAuth:
    """Create mock auth service that returns a fake token."""
    auth = SkogsstyrelsenAuth(test_settings)
    # Mock the get_token method to avoid real OAuth calls
    auth.get_token = AsyncMock(return_value="mock_access_token")
    return auth


@pytest.fixture
def mock_api_client(mock_auth: SkogsstyrelsenAuth, test_settings: Settings) -> SkogsstyrelsenClient:
    """Create mock API client with mocked auth."""
    return SkogsstyrelsenClient(mock_auth, test_settings)


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Create FastAPI test client."""
    # Override settings to use test credentials
    os.environ["SKOGSSTYRELSEN_CLIENT_ID"] = "test_client_id"
    os.environ["SKOGSSTYRELSEN_CLIENT_SECRET"] = "test_client_secret"

    # Clear any existing overrides
    app.dependency_overrides.clear()

    with TestClient(app) as test_client:
        yield test_client

    # Clean up overrides after test
    app.dependency_overrides.clear()


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Create async HTTP client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


# Example WKT geometries for testing
EXAMPLE_SMALL_POLYGON = "POLYGON ((485486 7018193, 486179 7018193, 486179 7018896, 485486 7018896, 485486 7018193))"
EXAMPLE_MULTIPOLYGON = "MULTIPOLYGON (((485486 7018193, 486179 7018193, 486179 7018896, 485486 7018896, 485486 7018193)))"
