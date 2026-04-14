# app/services/user_service.py
# ---------------------------------------------------------------
# Service layer — contains all business logic for Users.
# Routes call services; services talk to the database.
# This separation makes logic easy to test independently.
# ---------------------------------------------------------------

from sqlalchemy.orm import Session

from app.logger import logger
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate


class UserService:
    """All CRUD operations for the User resource."""

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------
    def create_user(self, db: Session, payload: UserCreate) -> User:
        """
        Create a new user record.
        Raises ValueError if username or email already exists.
        """
        logger.info(f"Creating user with username='{payload.username}'")

        # Check for duplicate username
        if db.query(User).filter(User.username == payload.username).first():
            logger.warning(f"Username '{payload.username}' already taken")
            raise ValueError(f"Username '{payload.username}' is already taken.")

        # Check for duplicate email
        if db.query(User).filter(User.email == payload.email).first():
            logger.warning(f"Email '{payload.email}' already registered")
            raise ValueError(f"Email '{payload.email}' is already registered.")

        # Build ORM object from validated Pydantic data
        new_user = User(**payload.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)  # Load DB-generated fields (id, created_at, etc.)

        logger.info(f"User created successfully: id={new_user.id}")
        return new_user

    # ------------------------------------------------------------------
    # READ — list
    # ------------------------------------------------------------------
    def get_users(self, db: Session, skip: int = 0, limit: int = 100) -> list[User]:
        """Return a paginated list of all users."""
        logger.info(f"Fetching users (skip={skip}, limit={limit})")
        return db.query(User).offset(skip).limit(limit).all()

    # ------------------------------------------------------------------
    # READ — single
    # ------------------------------------------------------------------
    def get_user(self, db: Session, user_id: int) -> User | None:
        """Return a single user by primary key, or None if not found."""
        logger.info(f"Fetching user id={user_id}")
        return db.query(User).filter(User.id == user_id).first()

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------
    def update_user(
        self, db: Session, user_id: int, payload: UserUpdate
    ) -> User | None:
        """
        Partially update a user. Only supplied fields are changed.
        Returns None if user is not found.
        """
        logger.info(f"Updating user id={user_id}")
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            logger.warning(f"User id={user_id} not found for update")
            return None

        # model_dump(exclude_unset=True) → only fields the caller provided
        update_data = payload.model_dump(exclude_unset=True)

        # Check uniqueness constraints for changed fields
        if "username" in update_data:
            conflict = (
                db.query(User)
                .filter(User.username == update_data["username"], User.id != user_id)
                .first()
            )
            if conflict:
                raise ValueError(
                    f"Username '{update_data['username']}' is already taken."
                )

        if "email" in update_data:
            conflict = (
                db.query(User)
                .filter(User.email == update_data["email"], User.id != user_id)
                .first()
            )
            if conflict:
                raise ValueError(
                    f"Email '{update_data['email']}' is already registered."
                )

        # Apply changes dynamically
        for field, value in update_data.items():
            setattr(user, field, value)

        db.commit()
        db.refresh(user)

        logger.info(f"User id={user_id} updated successfully")
        return user

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------
    def delete_user(self, db: Session, user_id: int) -> bool:
        """
        Delete a user by ID.
        Returns True if deleted, False if not found.
        """
        logger.info(f"Deleting user id={user_id}")
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            logger.warning(f"User id={user_id} not found for deletion")
            return False

        db.delete(user)
        db.commit()

        logger.info(f"User id={user_id} deleted successfully")
        return True


# Single shared instance
user_service = UserService()