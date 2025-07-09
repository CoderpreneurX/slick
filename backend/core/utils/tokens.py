"""
This module contains utility functions for handling tokens.
"""

from datetime import datetime, timedelta

from fastapi import status
from jose import JWTError, jwt

from core.config import get_settings
from core.exceptions import JSONException

settings = get_settings()


def create_access_token(data: dict) -> str:
    """
    Create an access token for the given data.

    Args:
        data (dict): The data to be encoded in the access token.

    Returns:
        str: The access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "token_type": "access"})
    encoded_jwt = jwt.encode(
        to_encode, settings.ACCESS_TOKEN_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Create a refresh token for the given data.

    Args:
        data (dict): The data to be encoded in the refresh token.

    Returns:
        str: The refresh token.
    """

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "token_type": "refresh"})
    encoded_jwt = jwt.encode(
        to_encode, settings.REFRESH_TOKEN_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def _decode_token(token: str, key: str):
    """
    Decode a token.

    Args:
        token (str): The token to decode.

    Returns:
        dict: The decoded token data.

    Raises:
        JWTError: If the token is invalid.
    """
    return jwt.decode(
        token, key, algorithms=[settings.JWT_ALGORITHM]
    )


def refresh_access_token(refresh_token: str) -> str:
    """
    Refresh an access token with the given refresh token.

    Args:
        refresh_token (str): The refresh token.

    Returns:
        str: The new access token.

    Raises:
        JSONException: If the refresh token is invalid or not a refresh token,
            or if the token payload is invalid.
    """
    try:
        payload = _decode_token(token=refresh_token, key=settings.REFRESH_TOKEN_SECRET_KEY)
    except JWTError as exc:
        raise JSONException(
            status_code=status.HTTP_401_UNAUTHORIZED, message="Invalid refresh token"
        ) from exc

    if payload.get("token_type") != "refresh":
        raise JSONException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Token is not a refresh token",
        )

    user_id = payload.get("sub")
    if not user_id:
        raise JSONException(
            status_code=status.HTTP_401_UNAUTHORIZED, message="Invalid token payload"
        )

    new_access_token = create_access_token({"sub": user_id})
    return new_access_token
