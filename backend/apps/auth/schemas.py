"""
This module contains the Pydantic Schemas for the Auth Requests and Responses.
"""

from typing import Optional

from pydantic import BaseModel, EmailStr


class RegisterUserPayload(BaseModel):
    """
    Pydantic model for registering a new user.
    """

    fullname: str
    username: str
    email: Optional[EmailStr] = None
    password: str


class LoginUserPayload(BaseModel):
    """
    Pydantic model for logging in a user.
    """

    username_or_email: str
    password: str


class UserDataResponse(BaseModel):
    """
    Pydantic model for user data response.
    """

    fullname: str
    username: str
    email: Optional[EmailStr] = None

    class Config:
        """
        Config class for user data response.
        """

        from_attributes = True
