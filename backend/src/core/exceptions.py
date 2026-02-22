"""
Global exception handlers for FastAPI.

This module defines custom exceptions and handlers for consistent error responses.
"""

from typing import Any, Dict

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


class TextbookGenerationException(Exception):
    """Base exception for textbook generation errors."""

    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class DatabaseError(TextbookGenerationException):
    """Database operation error."""

    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NotFoundError(TextbookGenerationException):
    """Resource not found error."""

    def __init__(self, resource: str, resource_id: Any):
        message = f"{resource} with id {resource_id} not found"
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)


class UnauthorizedError(TextbookGenerationException):
    """Unauthorized access error."""

    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)


class ForbiddenError(TextbookGenerationException):
    """Forbidden access error."""

    def __init__(self, message: str = "Access forbidden"):
        super().__init__(message, status_code=status.HTTP_403_FORBIDDEN)


class ValidationError(TextbookGenerationException):
    """Request validation error."""

    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ContentModerationError(TextbookGenerationException):
    """Content failed moderation check."""

    def __init__(self, message: str = "Content failed moderation check"):
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST)


class GenerationError(TextbookGenerationException):
    """AI content generation error."""

    def __init__(self, message: str = "Content generation failed"):
        super().__init__(message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExportError(TextbookGenerationException):
    """Export operation error."""

    def __init__(self, message: str = "Export operation failed"):
        super().__init__(message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Exception handlers


async def textbook_generation_exception_handler(
    request: Request, exc: TextbookGenerationException
) -> JSONResponse:
    """Handle custom TextbookGenerationException errors."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "path": str(request.url),
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle FastAPI HTTPException errors."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTPException",
            "message": exc.detail,
            "path": str(request.url),
        },
    )


async def sqlalchemy_exception_handler(
    request: Request, exc: SQLAlchemyError
) -> JSONResponse:
    """Handle SQLAlchemy database errors."""
    # Check for specific error types
    if isinstance(exc, IntegrityError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": "IntegrityError",
                "message": "Database integrity constraint violation",
                "path": str(request.url),
            },
        )

    # Generic database error
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "DatabaseError",
            "message": "Database operation failed",
            "path": str(request.url),
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred",
            "path": str(request.url),
        },
    )


def register_exception_handlers(app) -> None:
    """
    Register all exception handlers with the FastAPI app.

    Should be called during application setup.

    Args:
        app: FastAPI application instance
    """
    app.add_exception_handler(TextbookGenerationException, textbook_generation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
