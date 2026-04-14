# app/services/task_service.py
# ---------------------------------------------------------------
# Service layer for Task CRUD operations.
# ---------------------------------------------------------------

from sqlalchemy.orm import Session

from app.logger import logger
from app.models.task_model import Task
from app.schemas.task_schema import TaskCreate, TaskUpdate


class TaskService:
    """All CRUD operations for the Task resource."""

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------
    def create_task(self, db: Session, owner_id: int, payload: TaskCreate) -> Task:
        """Create a new task owned by `owner_id`."""
        logger.info(f"Creating task for user id={owner_id}: title='{payload.title}'")

        new_task = Task(**payload.model_dump(), owner_id=owner_id)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        logger.info(f"Task created: id={new_task.id}")
        return new_task

    # ------------------------------------------------------------------
    # READ — list by owner
    # ------------------------------------------------------------------
    def get_tasks_by_user(
        self, db: Session, owner_id: int, skip: int = 0, limit: int = 100
    ) -> list[Task]:
        """Return all tasks belonging to a specific user."""
        logger.info(f"Fetching tasks for user id={owner_id}")
        return (
            db.query(Task)
            .filter(Task.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # ------------------------------------------------------------------
    # READ — all tasks (admin use)
    # ------------------------------------------------------------------
    def get_all_tasks(self, db: Session, skip: int = 0, limit: int = 100) -> list[Task]:
        """Return all tasks across all users (paginated)."""
        logger.info(f"Fetching all tasks (skip={skip}, limit={limit})")
        return db.query(Task).offset(skip).limit(limit).all()

    # ------------------------------------------------------------------
    # READ — single
    # ------------------------------------------------------------------
    def get_task(self, db: Session, task_id: int) -> Task | None:
        """Return a single task by ID, or None if not found."""
        logger.info(f"Fetching task id={task_id}")
        return db.query(Task).filter(Task.id == task_id).first()

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------
    def update_task(
        self, db: Session, task_id: int, payload: TaskUpdate
    ) -> Task | None:
        """Partially update a task. Returns None if not found."""
        logger.info(f"Updating task id={task_id}")
        task = db.query(Task).filter(Task.id == task_id).first()

        if not task:
            logger.warning(f"Task id={task_id} not found for update")
            return None

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(task, field, value)

        db.commit()
        db.refresh(task)

        logger.info(f"Task id={task_id} updated successfully")
        return task

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------
    def delete_task(self, db: Session, task_id: int) -> bool:
        """Delete a task. Returns True if deleted, False if not found."""
        logger.info(f"Deleting task id={task_id}")
        task = db.query(Task).filter(Task.id == task_id).first()

        if not task:
            logger.warning(f"Task id={task_id} not found for deletion")
            return False

        db.delete(task)
        db.commit()

        logger.info(f"Task id={task_id} deleted successfully")
        return True


# Single shared instance
task_service = TaskService()