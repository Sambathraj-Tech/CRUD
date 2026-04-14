"""Model package exports.

Import ORM models here so `import app.models` registers every table with
SQLAlchemy metadata before `Base.metadata.create_all()` or Alembic autogenerate
runs.
"""

from app.models.task_model import Task  # noqa: F401
from app.models.user_model import User  # noqa: F401

