from __future__ import annotations

from typing import Any

import httpx

from backend.core.config import Settings
from backend.core.exceptions import APIError
from backend.core.logging import get_logger
from backend.services.auth import SkogsstyrelsenAuth

logger = get_logger(__name__)


class SkogsstyrelsenClient:
    """Client for interacting with Skogsstyrelsen APIs with connection pooling."""

    def __init__(self, auth: SkogsstyrelsenAuth, settings: Settings) -> None:
        self.auth = auth
        self.settings = settings
        self._http_client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create reusable HTTP client with connection pooling."""
        if self._http_client is None or self._http_client.is_closed:
            self._http_client = httpx.AsyncClient(
                timeout=self.settings.request_timeout,
                limits=httpx.Limits(
                    max_connections=self.settings.http_max_connections,
                    max_keepalive_connections=self.settings.http_max_keepalive_connections,
                ),
            )
        return self._http_client

    async def close(self) -> None:
        """Close HTTP client and release connections."""
        if self._http_client and not self._http_client.is_closed:
            await self._http_client.aclose()
            self._http_client = None

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make authenticated request to Skogsstyrelsen API."""
        token = await self.auth.get_token()
        headers = self.auth.get_auth_header(token)

        url = f"{self.settings.skogsstyrelsen_base_url}{endpoint}"
        logger.debug(f"Making {method} request to {url}")

        try:
            client = await self._get_client()
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json_data,
            )
            response.raise_for_status()
            logger.debug(f"Request successful: {method} {url}")
            return response.json()

        except httpx.HTTPStatusError as e:
            logger.error(f"API request failed: {e.response.status_code} - {e.response.text}")
            raise APIError(
                f"API request failed: {e.response.text}",
                status_code=e.response.status_code,
            )
        except httpx.RequestError as e:
            logger.error(f"Request error: {str(e)}")
            raise APIError(f"Request failed: {str(e)}")

    async def get(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Make GET request."""
        return await self._request("GET", endpoint, params=params)

    async def post(
        self, endpoint: str, json_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Make POST request."""
        return await self._request("POST", endpoint, json_data=json_data)
