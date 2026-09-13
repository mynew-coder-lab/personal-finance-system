"""
User service — business logic for user operations.

Handles registration, authentication, profile retrieval, and updates.
All password operations go through security utilities; plaintext is never stored.
"""

from sqlalchemy.orm import Session

from app.backend.models.user import User
from app.backend.schemas.user import UserCreate, UserUpdate
from app.backend.utils.exceptions import DuplicateException, NotFoundException
from app.backend.utils.security import hash_password, verify_password


def get_user_by_email(db: Session, email: str) -> User | None:
    """Find a user by email address."""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """Find a user by primary key."""
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, data: UserCreate) -> User:
    """
    Register a new user.

    Raises:
        DuplicateException: If email is already registered.
    """
    existing = get_user_by_email(db, data.email)
    if existing:
        raise DuplicateException("User", "Email already registered")

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        full_name=data.full_name,
        currency=data.currency,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """
    Verify credentials and return the user if valid.

    Returns None if email not found or password doesn't match.
    """
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def update_user(db: Session, user: User, data: UserUpdate) -> User:
    """Update user profile fields (only non-None fields are applied)."""
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user
