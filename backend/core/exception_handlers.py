import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.schemas.common import (
    APIErrorBody,
    APIErrorDetail,
    APIErrorResponse,
)

logger = logging.getLogger(__name__)


HTTP_ERROR_CODES = {
    400: ("BAD_REQUEST", "Bad request"),
    401: ("UNAUTHORIZED", "Authentication is required"),
    403: ("FORBIDDEN", "You do not have permission to perform this action"),
    404: ("NOT_FOUND", "Resource not found"),
    405: ("METHOD_NOT_ALLOWED", "Method not allowed"),
    409: ("CONFLICT", "Request conflicts with current resource state"),
    413: ("PAYLOAD_TOO_LARGE", "Request body is too large"),
    415: ("UNSUPPORTED_MEDIA_TYPE", "Unsupported media type"),
    429: ("TOO_MANY_REQUESTS", "Too many requests"),
}


def _error_response(
    status_code: int,
    code: str,
    message: str,
    details: list[APIErrorDetail] | None = None,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    body = APIErrorResponse(
        error=APIErrorBody(
            code=code,
            message=message,
            details=details or [],
        )
    )

    return JSONResponse(
        status_code=status_code,
        content=body.model_dump(mode="json"),
        headers=headers,
    )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        details = [
            APIErrorDetail(
                location=list(error.get("loc", [])),
                message=error.get("msg", "Invalid input"),
                type=error.get("type"),
            )
            for error in exc.errors()
        ]

        return _error_response(
            status_code=422,
            code="VALIDATION_ERROR",
            message="Request validation failed",
            details=details,
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request,
        exc: StarletteHTTPException,
    ) -> JSONResponse:
        if exc.status_code >= 500:
            code = "INTERNAL_SERVER_ERROR"
            message = "An unexpected error occurred"
        else:
            code, default_message = HTTP_ERROR_CODES.get(
                exc.status_code,
                ("HTTP_ERROR", "The request could not be completed"),
            )
            message = (
                exc.detail
                if isinstance(exc.detail, str)
                else default_message
            )

        return _error_response(
            status_code=exc.status_code,
            code=code,
            message=message,
            headers=exc.headers,
        )

    @app.exception_handler(Exception)
    async def unexpected_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        logger.error(
            "Unhandled exception while processing request",
            exc_info=(type(exc), exc, exc.__traceback__),
        )

        return _error_response(
            status_code=500,
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred",
        )