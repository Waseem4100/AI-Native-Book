"""
Standardized error response schemas.

This module defines Pydantic models for consistent error responses across the API.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """
    Detailed error information.

    Attributes:
        loc: Location of the error (e.g., field path for validation errors)
        msg: Error message
        type: Error type identifier
    """

    loc: Optional[List[str]] = Field(None, description="Error location (field path)")
    msg: str = Field(..., description="Error message")
    type: str = Field(..., description="Error type identifier")


class ErrorResponse(BaseModel):
    """
    Standard error response format.

    Attributes:
        error: Error type/category
        message: Human-readable error message
        path: Request path where error occurred
        details: Additional error details (e.g., validation errors)
    """

    error: str = Field(..., description="Error type or category")
    message: str = Field(..., description="Human-readable error message")
    path: str = Field(..., description="Request path where error occurred")
    details: Optional[List[ErrorDetail]] = Field(
        None, description="Additional error details"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Request validation failed",
                "path": "/api/v1/textbooks/generate-outline",
                "details": [
                    {
                        "loc": ["body", "subject"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ],
            }
        }


class NotFoundResponse(BaseModel):
    """404 Not Found response."""

    error: str = Field(default="NotFoundError", description="Error type")
    message: str = Field(..., description="Resource not found message")
    path: str = Field(..., description="Request path")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "NotFoundError",
                "message": "Textbook with id 123 not found",
                "path": "/api/v1/textbooks/123",
            }
        }


class UnauthorizedResponse(BaseModel):
    """401 Unauthorized response."""

    error: str = Field(default="UnauthorizedError", description="Error type")
    message: str = Field(..., description="Unauthorized access message")
    path: str = Field(..., description="Request path")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "UnauthorizedError",
                "message": "Invalid authentication token",
                "path": "/api/v1/textbooks/me",
            }
        }


class ForbiddenResponse(BaseModel):
    """403 Forbidden response."""

    error: str = Field(default="ForbiddenError", description="Error type")
    message: str = Field(..., description="Forbidden access message")
    path: str = Field(..., description="Request path")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "ForbiddenError",
                "message": "Access forbidden",
                "path": "/api/v1/textbooks/123",
            }
        }


class ValidationErrorResponse(BaseModel):
    """422 Validation Error response."""

    error: str = Field(default="ValidationError", description="Error type")
    message: str = Field(..., description="Validation error message")
    path: str = Field(..., description="Request path")
    details: List[ErrorDetail] = Field(..., description="Field-level validation errors")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Request validation failed",
                "path": "/api/v1/textbooks/generate-outline",
                "details": [
                    {
                        "loc": ["body", "subject"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                    {
                        "loc": ["body", "level"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                ],
            }
        }


class InternalServerErrorResponse(BaseModel):
    """500 Internal Server Error response."""

    error: str = Field(default="InternalServerError", description="Error type")
    message: str = Field(
        default="An unexpected error occurred", description="Error message"
    )
    path: str = Field(..., description="Request path")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "InternalServerError",
                "message": "An unexpected error occurred",
                "path": "/api/v1/generation/generate-chapter",
            }
        }


# Common error response documentation for OpenAPI
COMMON_RESPONSES: Dict[int, Dict[str, Any]] = {
    400: {
        "model": ErrorResponse,
        "description": "Bad Request - Invalid request parameters",
    },
    401: {
        "model": UnauthorizedResponse,
        "description": "Unauthorized - Authentication required",
    },
    403: {
        "model": ForbiddenResponse,
        "description": "Forbidden - Insufficient permissions",
    },
    404: {
        "model": NotFoundResponse,
        "description": "Not Found - Resource does not exist",
    },
    422: {
        "model": ValidationErrorResponse,
        "description": "Validation Error - Request validation failed",
    },
    500: {
        "model": InternalServerErrorResponse,
        "description": "Internal Server Error - Unexpected server error",
    },
}
