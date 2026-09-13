"""
Authentication dependencies for protected routes.

Provides get_current_user — extracts and validates the JWT from the
Authorization: Bearer header and returns the authenticated User.
"""

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.backend.config import settings
from app.backend.database.dependencies import get_db
from app.backend.models.user import User
from app.backend.utils.exceptions import CredentialsException
from app.backend.utils.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Dependency: extract user from JWT token.

    Raises CredentialsException if token is invalid, expired, or user not found.
    """
    try:
        payload = decode_access_token(token)
        user_id: int | None = payload.get("sub")
        if user_id is None:
            raise CredentialsException()
    except jwt.ExpiredSignatureError:
        raise CredentialsException("Token has expired")
    except jwt.InvalidTokenError:
        raise CredentialsException()

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise CredentialsException("User not found")
    if not user.is_active:
        raise CredentialsException("User account is inactive")

    return user
