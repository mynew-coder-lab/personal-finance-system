"""
Consistent exception classes for the application.

Returns safe client-facing errors while logging diagnostics internally.
"""

from fastapi import HTTPException, status


class AppException(HTTPException):
    """Base application exception."""

    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: dict[str, str] | None = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


# ── Authentication / Authorization ───────────────────────────────


class CredentialsException(AppException):
    """Invalid or missing authentication credentials."""

    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class ForbiddenException(AppException):
    """User lacks permission to access this resource."""

    def __init__(self, detail: str = "Not authorized to access this resource"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


# ── Resource Errors ──────────────────────────────────────────────


class NotFoundException(AppException):
    """Requested resource was not found."""

    def __init__(self, resource: str = "Resource", detail: str | None = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail or f"{resource} not found",
        )


class DuplicateException(AppException):
    """Resource already exists."""

    def __init__(self, resource: str = "Resource", detail: str | None = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail or f"{resource} already exists",
        )


# ── Validation ───────────────────────────────────────────────────


class ValidationException(AppException):
    """Invalid input data."""

    def __init__(self, detail: str = "Invalid input data"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
        )
