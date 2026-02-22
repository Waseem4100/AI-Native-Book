"""
Pydantic schemas package.

Exports all API request/response schemas.
"""

from .errors import (
    COMMON_RESPONSES,
    ErrorResponse,
    ForbiddenResponse,
    InternalServerErrorResponse,
    NotFoundResponse,
    UnauthorizedResponse,
    ValidationErrorResponse,
)
from .textbook import (
    ChapterOutline,
    SectionOutline,
    TextbookCreate,
    TextbookResponse,
    TextbookUpdate,
)

__all__ = [
    # Error schemas
    "ErrorResponse",
    "NotFoundResponse",
    "UnauthorizedResponse",
    "ForbiddenResponse",
    "ValidationErrorResponse",
    "InternalServerErrorResponse",
    "COMMON_RESPONSES",
    # Textbook schemas
    "TextbookCreate",
    "TextbookResponse",
    "TextbookUpdate",
    "ChapterOutline",
    "SectionOutline",
]
