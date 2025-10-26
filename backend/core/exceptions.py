from __future__ import annotations


class SkogsstyrelsenError(Exception):
    """Base exception for Skogsstyrelsen API errors."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationError(SkogsstyrelsenError):
    """Authentication failed."""

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message, status_code=401)


class APIError(SkogsstyrelsenError):
    """External API request failed."""

    pass


class ConfigurationError(SkogsstyrelsenError):
    """Configuration error."""

    def __init__(self, message: str = "Configuration error") -> None:
        super().__init__(message, status_code=500)
