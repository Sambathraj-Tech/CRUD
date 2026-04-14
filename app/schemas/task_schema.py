# app/schemas/task.py
# ---------------------------------------------------------------
# Pydantic schemas for Task CRUD operations.
# ---------------------------------------------------------------

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    """Shared fields."""

    title: str = Field(..., min_length=1, max_length=200, examples=["Buy groceries"])
    description: str | None = Field(None, examples=["Milk, eggs, bread"])


class TaskCreate(TaskBase):
    """Schema for POST /users/{user_id}/tasks."""
    pass


class TaskUpdate(BaseModel):
    """Schema for PATCH /tasks/{id} — all fields optional."""

    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = None
    is_completed: bool | None = None


class TaskResponse(TaskBase):
    """Schema returned to the client."""

    id: int
    is_completed: bool
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)