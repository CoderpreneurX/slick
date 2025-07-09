"""
This module contains the Auth models.
"""

from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, String, func

from core.database import Base


class User(Base):
    """
    The User model.

    Attributes:
        id (str): The unique identifier for the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        password (str): The hashed password of the user.
        active (bool): Whether the user is active or not.
    """

    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    fullname = Column(String(50), nullable=True, default="Anonymous User")
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=True)
    password = Column(String(128), nullable=False)  # hashed password
    active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now()) # pylint: disable=not-callable
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now # pylint: disable=not-callable
    )
