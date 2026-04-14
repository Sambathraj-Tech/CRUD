# app/controllers/user_controller.py
# ---------------------------------------------------------------
# Controllers (route handlers) sit between the HTTP layer and
# the service layer. Their only job is to:
#   1. Receive and validate HTTP request data (done by FastAPI/Pydantic)
#   2. Call the appropriate service method
#   3. Return a properly formatted HTTP response
#
# Business logic does NOT live here — it lives in services.
# ---------------------------------------------------------------

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.logger import logger
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate
from app.services.user_service import user_service

# Create a router with a URL prefix and a tag for Swagger docs
router = APIRouter(prefix="/users", tags=["Users"])


# ---------------------------------------------------------------
# POST /users  →  Create a new user
# ---------------------------------------------------------------
@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account.

    - **username**: 3–50 characters, must be unique
    - **email**: valid email, must be unique
    - **full_name**: optional display name
    """
    try:
        return user_service.create_user(db, payload)
    except ValueError as exc:
        # ValueError from service = client's fault → 400 Bad Request
        logger.error(f"Create user validation error: {exc}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


# ---------------------------------------------------------------
# GET /users  →  List all users (paginated)
# ---------------------------------------------------------------
@router.get(
    "/",
    response_model=list[UserResponse],
    summary="List all users",
)
def list_users(
    skip: int = Query(default=0, ge=0, description="Records to skip"),
    limit: int = Query(default=10, ge=1, le=100, description="Max records to return"),
    db: Session = Depends(get_db),
):
    """
    Retrieve a paginated list of users.

    - **skip**: offset (default 0)
    - **limit**: page size, max 100 (default 10)
    """
    return user_service.get_users(db, skip=skip, limit=limit)


# ---------------------------------------------------------------
# GET /users/{user_id}  →  Get a single user
# ---------------------------------------------------------------
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get a user by ID",
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Retrieve a single user by their numeric ID."""
    user = user_service.get_user(db, user_id)
    if not user:
        logger.warning(f"User id={user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id={user_id} not found.",
        )
    return user


# ---------------------------------------------------------------
# PATCH /users/{user_id}  →  Partially update a user
# ---------------------------------------------------------------
@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update a user",
)
def update_user(
    user_id: int, payload: UserUpdate, db: Session = Depends(get_db)
):
    """
    Partially update a user. Only include the fields you want to change.
    """
    try:
        user = user_service.update_user(db, user_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id={user_id} not found.",
        )
    return user


# ---------------------------------------------------------------
# DELETE /users/{user_id}  →  Delete a user
# ---------------------------------------------------------------
@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Permanently delete a user and all their tasks (cascade).
    Returns 204 No Content on success.
    """
    deleted = user_service.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id={user_id} not found.",
        )
    # FastAPI automatically returns 204 with no body