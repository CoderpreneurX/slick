"""
This module contains the functions to handle the cookies.
"""

from fastapi.responses import JSONResponse

from apps.auth.models import User

from .tokens import create_access_token, create_refresh_token


def set_auth_cookies(response: JSONResponse, user: User):
    """
    Set access and refresh tokens in the response cookies.

    Args:
        response (JSONResponse): The JSONResponse to set the cookies in.
        user (User): The user to set the cookies for.

    Returns:
        JSONResponse: The JSONResponse with the cookies set.
    """
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)

    return response
