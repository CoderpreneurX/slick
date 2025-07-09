"""
This module contains dependencies for the application.
"""

from fastapi import Depends, Request, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from apps.auth.crud import read_user_by_id
from apps.auth.models import User
from core.config import get_settings
from core.database import get_session
from core.exceptions import JSONException

settings = get_settings()

SECRET_KEY = settings.ACCESS_TOKEN_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM


def get_current_user(request: Request, session: Session = Depends(get_session)) -> User:
    """
    Dependency to get the current user from the request cookies.
    """
    token = request.cookies.get("access_token")

    if not token:
        raise JSONException(
            message="Authentication token is missing from cookies.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise JSONException(
                "Invalid token payload.", status_code=status.HTTP_401_UNAUTHORIZED
            )
    except JWTError as exc:
        raise JSONException(
            "Could not validate credentials.", status_code=status.HTTP_401_UNAUTHORIZED
        ) from exc

    user = read_user_by_id(session=session, user_id=user_id)
    if user is None:
        raise JSONException("User not found.", status_code=status.HTTP_404_NOT_FOUND)

    return user
