from __future__ import annotations

import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Skogsstyrelsen API credentials
    skogsstyrelsen_client_id: str
    skogsstyrelsen_client_secret: str

    # API URLs
    skogsstyrelsen_base_url: str = "https://api.skogsstyrelsen.se/sksapi"
    skogsstyrelsen_auth_url: str = "https://auth.skogsstyrelsen.se/connect/token"

    # Application settings
    app_title: str = "Skogsstyrelsen API Gateway"
    app_version: str = "0.1.0"
    debug: bool = False

    # CORS settings
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:4173"]

    # Request timeout
    request_timeout: float = 30.0

    # HTTP client connection pooling
    http_max_connections: int = 100
    http_max_keepalive_connections: int = 20

    # Authentication settings
    auth_request_timeout: float = 10.0
    token_refresh_buffer_minutes: int = 5  # Refresh token N minutes before expiry


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
