# app/controllers/task_controller.py
# ---------------------------------------------------------------
# Route handlers for Task CRUD operations.
# ---------------------------------------------------------------

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.logger import logger
from app.schemas.task_schema import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import task_service
from app.services.user_service import user_service

router = APIRouter(tags=["Tasks"])


# ---------------------------------------------------------------
# POST /users/{user_id}/tasks  →  Create a task for a user
# ---------------------------------------------------------------
@router.post(
    "/users/{user_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a task for a user",
)
def create_task(
    user_id: int, payload: TaskCreate, db: Session = Depends(get_db)
):
    """
    Create a new task owned by the specified user.

    - **title**: required, 1–200 characters
    - **description**: optional longer description
    """
    # Verify the owner exists before creating the task
    owner = user_service.get_user(db, user_id)
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id={user_id} not found.",
        )

    return task_service.create_task(db, owner_id=user_id, payload=payload)


# ---------------------------------------------------------------
# GET /users/{user_id}/tasks  →  List tasks for a user
# ---------------------------------------------------------------
@router.get(
    "/users/{user_id}/tasks",
    response_model=list[TaskResponse],
    summary="List tasks for a user",
)
def list_user_tasks(
    user_id: int,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Retrieve all tasks belonging to a specific user (paginated)."""
    owner = user_service.get_user(db, user_id)
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id={user_id} not found.",
        )
    return task_service.get_tasks_by_user(db, owner_id=user_id, skip=skip, limit=limit)


# ---------------------------------------------------------------
# GET /tasks  →  List all tasks
# ---------------------------------------------------------------
@router.get(
    "/tasks",
    response_model=list[TaskResponse],
    summary="List all tasks",
)
def list_all_tasks(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Retrieve all tasks across all users (paginated)."""
    return task_service.get_all_tasks(db, skip=skip, limit=limit)


# ---------------------------------------------------------------
# GET /tasks/{task_id}  →  Get a single task
# ---------------------------------------------------------------
@router.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Get a task by ID",
)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Retrieve a single task by its numeric ID."""
    task = task_service.get_task(db, task_id)
    if not task:
        logger.warning(f"Task id={task_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id={task_id} not found.",
        )
    return task


# ---------------------------------------------------------------
# PATCH /tasks/{task_id}  →  Update a task
# ---------------------------------------------------------------
@router.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
)
def update_task(
    task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)
):
    """Partially update a task. Only include fields you want to change."""
    task = task_service.update_task(db, task_id, payload)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id={task_id} not found.",
        )
    return task


# ---------------------------------------------------------------
# DELETE /tasks/{task_id}  →  Delete a task
# ---------------------------------------------------------------
@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Permanently delete a task by ID. Returns 204 No Content."""
    deleted = task_service.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id={task_id} not found.",
        )