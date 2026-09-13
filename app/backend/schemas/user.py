"""
User Pydantic schemas for request/response validation.
"""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# ── Request Schemas ──────────────────────────────────────────────


class UserCreate(BaseModel):
    """Registration request."""
    email: str = Field(..., max_length=255, examples=["user@example.com"])
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str = Field(..., min_length=1, max_length=255, examples=["John Doe"])
    currency: str = Field(default="INR", max_length=10)


class UserUpdate(BaseModel):
    """Profile update request (partial)."""
    full_name: str | None = Field(default=None, min_length=1, max_length=255)
    currency: str | None = Field(default=None, max_length=10)


class UserLogin(BaseModel):
    """Login request."""
    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=1)


# ── Response Schemas ─────────────────────────────────────────────


class UserResponse(BaseModel):
    """User profile response (never includes password)."""
    id: int
    email: str
    full_name: str
    currency: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"
