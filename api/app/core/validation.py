"""
Password validation utilities.

This module provides password strength validation according to
enterprise security standards.
"""

import re
from typing import List

from app.core.config import settings
from app.core.exceptions import ValidationException


def validate_password_strength(password: str) -> None:
    """Validate password meets strength requirements."""
    errors: List[str] = []
    
    if len(password) < settings.PASSWORD_MIN_LENGTH:
        errors.append(f"Password must be at least {settings.PASSWORD_MIN_LENGTH} characters")
    
    if settings.PASSWORD_REQUIRE_UPPERCASE and not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter")
    
    if settings.PASSWORD_REQUIRE_LOWERCASE and not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one lowercase letter")
    
    if settings.PASSWORD_REQUIRE_NUMBER and not re.search(r"\d", password):
        errors.append("Password must contain at least one number")
    
    if settings.PASSWORD_REQUIRE_SPECIAL and not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        errors.append("Password must contain at least one special character")
    
    if errors:
        raise ValidationException(
            message="Password does not meet strength requirements",
            details={"errors": errors},
        )


def validate_email(email: str) -> None:
    """Validate email format."""
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_pattern, email):
        raise ValidationException(
            message="Invalid email format",
            details={"field": "email"},
        )

