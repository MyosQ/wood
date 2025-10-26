from __future__ import annotations

from functools import lru_cache

from backend.core.config import Settings, get_settings
from backend.services.auth import SkogsstyrelsenAuth
from backend.services.skogsstyrelsen_client import SkogsstyrelsenClient


@lru_cache
def get_auth_service() -> SkogsstyrelsenAuth:
    """Get singleton auth service instance."""
    settings = get_settings()
    return SkogsstyrelsenAuth(settings)


def get_api_client() -> SkogsstyrelsenClient:
    """Get API client with dependencies."""
    settings = get_settings()
    auth = get_auth_service()
    return SkogsstyrelsenClient(auth, settings)
