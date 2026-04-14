# app/models/task.py
# ---------------------------------------------------------------
# SQLAlchemy ORM model for the "tasks" table.
# ---------------------------------------------------------------

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Task(Base):
    """
    Represents a task assigned to a user.

    Table: tasks
    """

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Short task title
    title: Mapped[str] = mapped_column(String(200), nullable=False)

    # Optional longer description
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Whether the task has been completed
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Foreign key — every task belongs to a user
    # ON DELETE CASCADE: deleting a user removes all their tasks
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Many-to-one: each task has one owner
    owner: Mapped["User"] = relationship("User", back_populates="tasks")  # noqa: F821

    def __repr__(self) -> str:
        return f"<Task id={self.id} title={self.title!r} owner_id={self.owner_id}>"