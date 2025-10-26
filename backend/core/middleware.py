from __future__ import annotations

from uuid import uuid4

from fastapi import Request, status
from fastapi.responses import JSONResponse

from backend.core.exceptions import (
    APIError,
    AuthenticationError,
    ConfigurationError,
    SkogsstyrelsenError,
)
from backend.core.logging import get_logger

logger = get_logger(__name__)


async def request_id_middleware(request: Request, call_next):
    """Add request ID for distributed tracing."""
    request_id = request.headers.get("X-Request-ID") or str(uuid4())
    request.state.request_id = request_id

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


async def error_handler_middleware(request: Request, call_next):
    """Global error handling middleware with enhanced context."""
    request_id = getattr(request.state, "request_id", "unknown")

    try:
        return await call_next(request)
    except AuthenticationError as e:
        logger.error(f"[{request_id}] Authentication error: {e.message}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "detail": e.message,
                "type": "authentication_error",
                "request_id": request_id,
            },
        )
    except ConfigurationError as e:
        logger.error(f"[{request_id}] Configuration error: {e.message}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": e.message,
                "type": "configuration_error",
                "request_id": request_id,
            },
        )
    except APIError as e:
        logger.error(f"[{request_id}] API error: {e.message}")
        return JSONResponse(
            status_code=e.status_code or status.HTTP_502_BAD_GATEWAY,
            content={
                "detail": e.message,
                "type": "api_error",
                "status_code": e.status_code,
                "request_id": request_id,
            },
        )
    except SkogsstyrelsenError as e:
        logger.error(f"[{request_id}] Skogsstyrelsen error: {e.message}")
        return JSONResponse(
            status_code=e.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": e.message,
                "type": "skogsstyrelsen_error",
                "request_id": request_id,
            },
        )
    except Exception as e:
        logger.exception(f"[{request_id}] Unhandled exception: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Internal server error",
                "type": "internal_error",
                "request_id": request_id,
            },
        )
