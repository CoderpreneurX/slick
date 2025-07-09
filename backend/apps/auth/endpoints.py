"""
This module contains the endpoints for the auth module.
"""

from fastapi import Depends, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from apps.auth.models import User
from apps.auth.schemas import LoginUserPayload, RegisterUserPayload, UserDataResponse
from apps.auth.services import (
    handle_login_user,
    handle_refresh_access_token,
    handle_register_user,
)
from core.database import get_session
from core.dependencies import get_current_user
from core.utils.cookies import set_auth_cookies


def register_user_endpoint(
    data: RegisterUserPayload, session: Session = Depends(get_session)
):
    """
    Endpoint to register a new user.
    """
    handle_register_user(data=data, session=session)

    return JSONResponse(
        content={
            "success": True,
            "message": "Registration successful!",
        },
        status_code=status.HTTP_201_CREATED,
    )


def login_user_endpoint(
    data: LoginUserPayload, session: Session = Depends(get_session)
):
    """
    Endpoint to login a user.
    """
    user = handle_login_user(data=data, session=session)

    response = JSONResponse(
        content={
            "success": True,
            "message": "Login successful!",
            "data": UserDataResponse.model_validate(user).model_dump(mode="json"),
        },
        status_code=status.HTTP_200_OK,
    )

    response = set_auth_cookies(response=response, user=user)

    return response


def get_user_endpoint(user: User = Depends(get_current_user)):
    """
    Endpoint to get the current user.
    """
    return JSONResponse(
        content={
            "success": True,
            "message": "User retrieved successfully!",
            "data": UserDataResponse.model_validate(user).model_dump(mode="json"),
        },
        status_code=status.HTTP_200_OK,
    )


def refresh_access_token_endpoint(request: Request):
    """
    Endpoint to refresh the access token.
    """
    access_token = handle_refresh_access_token(request=request)
    response = JSONResponse(
        content={
            "success": True,
            "message": "Access token refreshed successfully!",
        },
        status_code=status.HTTP_200_OK,
    )

    response.set_cookie(key="access_token", value=access_token, httponly=True)

    return response
