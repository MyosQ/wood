from __future__ import annotations

from datetime import datetime, timedelta

import httpx

from backend.core.config import Settings
from backend.core.exceptions import AuthenticationError
from backend.core.logging import get_logger

logger = get_logger(__name__)


class SkogsstyrelsenAuth:
    """Handles OAuth2 authentication for Skogsstyrelsen APIs."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._access_token: str | None = None
        self._token_expiry: datetime | None = None

        if not settings.skogsstyrelsen_client_id or not settings.skogsstyrelsen_client_secret:
            raise AuthenticationError(
                "SKOGSSTYRELSEN_CLIENT_ID and SKOGSSTYRELSEN_CLIENT_SECRET must be set"
            )

    async def get_token(self) -> str:
        """Get valid access token, refreshing if necessary."""
        if self._is_token_valid():
            return self._access_token

        return await self._fetch_new_token()

    def _is_token_valid(self) -> bool:
        """Check if current token is still valid."""
        if not self._access_token or not self._token_expiry:
            return False

        # Refresh token before expiry (configurable buffer)
        buffer = timedelta(minutes=self.settings.token_refresh_buffer_minutes)
        return datetime.now() < (self._token_expiry - buffer)

    async def _fetch_new_token(self) -> str:
        """Fetch new access token from auth server."""
        logger.info("Fetching new OAuth2 token")

        try:
            async with httpx.AsyncClient(timeout=self.settings.auth_request_timeout) as client:
                response = await client.post(
                    self.settings.skogsstyrelsen_auth_url,
                    data={
                        "grant_type": "client_credentials",
                        "client_id": self.settings.skogsstyrelsen_client_id,
                        "client_secret": self.settings.skogsstyrelsen_client_secret,
                        "scope": "sks_api",
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )
                response.raise_for_status()

                data = response.json()
                self._access_token = data["access_token"]
                self._token_expiry = datetime.now() + timedelta(
                    seconds=data["expires_in"]
                )

                logger.info("Successfully obtained OAuth2 token")
                return self._access_token

        except httpx.HTTPStatusError as e:
            logger.error(f"Authentication failed: {e.response.status_code}")
            raise AuthenticationError(f"Failed to obtain token: {e.response.text}")
        except httpx.RequestError as e:
            logger.error(f"Request error during authentication: {e}")
            raise AuthenticationError(f"Authentication request failed: {str(e)}")

    def get_auth_header(self, token: str) -> dict[str, str]:
        """Get authorization header for API requests."""
        return {"Authorization": f"Bearer {token}"}
