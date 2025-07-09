"""
This module contains the services for the auth module.
"""

from typing import Any

from fastapi import Request
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from apps.auth.crud import create_user, read_user_by_username_or_email
from apps.auth.models import User
from apps.auth.schemas import LoginUserPayload, RegisterUserPayload
from core.exceptions import JSONException
from core.utils.tokens import refresh_access_token

# Use bcrypt hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _hash_password(raw_password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(raw_password)


def _verify_password(raw_password: str, hashed_password: str | Any) -> bool:
    """Verify a password using bcrypt."""
    return pwd_context.verify(raw_password, hashed_password)


def handle_register_user(data: RegisterUserPayload, session: Session) -> User:
    """
    Handle user registration.

    Args:
        data (RegisterUserPayload): The user registration data.
        session (Session): The database session.

    Returns:
        User: The newly created user.

    Raises:
        JSONException: If username or email is already taken.
    """
    username = data.username
    password = _hash_password(raw_password=data.password)
    email = data.email

    if read_user_by_username_or_email(session=session, username_or_email=username):
        raise JSONException(message="Username already taken!", status_code=400)

    if email and read_user_by_username_or_email(
        session=session, username_or_email=email
    ):
        raise JSONException(message="Email already taken!", status_code=400)

    return create_user(
        session=session, username=username, password_hash=password, email=email
    )


def handle_login_user(data: LoginUserPayload, session: Session) -> User:
    """
    Handle user login process.

    Args:
        data (LoginUserPayload): The login data containing username/email and password.
        session (Session): The database session.

    Returns:
        User: The authenticated user.

    Raises:
        JSONException: If the credentials are invalid.
    """

    user = read_user_by_username_or_email(
        session=session, username_or_email=data.username_or_email
    )

    if not user or not _verify_password(
        raw_password=data.password, hashed_password=user.password
    ):
        raise JSONException(message="Invalid Credentials!", status_code=401)

    return user


def handle_refresh_access_token(request: Request):
    """
    Handle the refresh of the access token.

    Args:
        user (User): The user object.
        session (Session): The database session.
    """
    refresh_token = request.cookies.get("refresh_token")

    print("Refresh token provided:", refresh_token)

    if not refresh_token:
        raise JSONException(message="Refresh token is missing!", status_code=401)

    return refresh_access_token(refresh_token=refresh_token)
