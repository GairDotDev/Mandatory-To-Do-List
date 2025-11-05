"""
Custom exception classes for the application.

This module defines custom exception classes that map to HTTP status codes
and provide structured error responses.
"""

from typing import Any, Dict, Optional


class AppException(Exception):
    """Base application exception."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "INTERNAL_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class BadRequestException(AppException):
    """400 Bad Request exception."""

    def __init__(self, message: str = "Bad request", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 400, "BAD_REQUEST", details)


class UnauthorizedException(AppException):
    """401 Unauthorized exception."""

    def __init__(self, message: str = "Unauthorized", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 401, "UNAUTHORIZED", details)


class ForbiddenException(AppException):
    """403 Forbidden exception."""

    def __init__(self, message: str = "Forbidden", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 403, "FORBIDDEN", details)


class NotFoundException(AppException):
    """404 Not Found exception."""

    def __init__(self, message: str = "Resource not found", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 404, "NOT_FOUND", details)


class ConflictException(AppException):
    """409 Conflict exception."""

    def __init__(self, message: str = "Resource conflict", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 409, "CONFLICT", details)


class ValidationException(AppException):
    """422 Unprocessable Entity exception."""

    def __init__(self, message: str = "Validation error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 422, "VALIDATION_ERROR", details)


class RateLimitException(AppException):
    """429 Too Many Requests exception."""

    def __init__(self, message: str = "Rate limit exceeded", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 429, "RATE_LIMIT_EXCEEDED", details)


class InternalServerException(AppException):
    """500 Internal Server Error exception."""

    def __init__(self, message: str = "Internal server error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 500, "INTERNAL_ERROR", details)

