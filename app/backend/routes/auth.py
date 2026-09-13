"""
Authentication routes: register, login, and current user profile.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.backend.database.dependencies import get_db
from app.backend.models.user import User
from app.backend.schemas.user import (
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
)
from app.backend.services.user_service import (
    authenticate_user,
    create_user,
    update_user,
)
from app.backend.utils.auth import get_current_user
from app.backend.utils.exceptions import CredentialsException
from app.backend.utils.logging import logger
from app.backend.utils.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user account."""
    user = create_user(db, data)
    logger.info("User registered: id=%d email=%s", user.id, user.email)
    return user


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return JWT access token."""
    user = authenticate_user(db, data.email, data.password)
    if not user:
        raise CredentialsException("Invalid email or password")

    access_token = create_access_token(data={"sub": user.id})
    logger.info("User logged in: id=%d", user.id)
    return TokenResponse(access_token=access_token)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user's profile."""
    return current_user


@router.patch("/me", response_model=UserResponse)
def update_me(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update current user's profile (full_name, currency)."""
    updated = update_user(db, current_user, data)
    return updated
