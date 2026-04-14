# app/models/user.py
# ---------------------------------------------------------------
# SQLAlchemy ORM model for the "users" table.
# This defines the actual database table schema.
# ---------------------------------------------------------------

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    """
    Represents a user in the database.

    Table: users
    """

    __tablename__ = "users"

    # Primary key — auto-incremented by the database
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Unique username (indexed for fast lookups)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )

    # Unique email
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )

    # Full display name (optional)
    full_name: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Whether the account is active (soft-delete pattern)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Timestamps — set automatically by the database
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # One-to-many: a user can have many tasks
    tasks: Mapped[list["Task"]] = relationship(  # noqa: F821
        "Task", back_populates="owner", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r}>"