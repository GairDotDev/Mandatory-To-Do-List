"""
Application routers module.

This module exports all routers for inclusion in the main application.
"""

from app.routers import auth, todos

__all__ = ["auth", "todos"]

