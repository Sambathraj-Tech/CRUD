# app/schemas/user.py
# ---------------------------------------------------------------
# Pydantic schemas validate incoming request data and shape
# outgoing response data. They are separate from ORM models.
#
# Pattern:
#   UserBase     → shared fields
#   UserCreate   → fields required when creating  (request body)
#   UserUpdate   → fields allowed when updating   (all optional)
#   UserResponse → fields returned to the client  (response body)
# ---------------------------------------------------------------

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """Fields shared across create / update / response schemas."""

    username: str = Field(..., min_length=3, max_length=50, examples=["john_doe"])
    email: EmailStr = Field(..., examples=["john@example.com"])
    full_name: str | None = Field(None, max_length=100, examples=["John Doe"])


class UserCreate(UserBase):
    """Schema for POST /users — all base fields are required."""
    pass


class UserUpdate(BaseModel):
    """
    Schema for PATCH /users/{id}.
    Every field is optional so callers can update only what changed.
    """

    username: str | None = Field(None, min_length=3, max_length=50)
    email: EmailStr | None = None
    full_name: str | None = Field(None, max_length=100)
    is_active: bool | None = None


class UserResponse(UserBase):
    """
    Schema returned to the client.
    Includes DB-generated fields (id, is_active, timestamps).
    """

    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    # Allow Pydantic to read values from ORM objects (not just dicts)
    model_config = ConfigDict(from_attributes=True)