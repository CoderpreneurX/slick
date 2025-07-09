"""
This module contains the CRUD operations for the User model.
"""

from typing import Optional

from sqlalchemy.orm import Session

from .models import User


def create_user(
    session: Session, username: str, password_hash: str, email: Optional[str] = None
) -> User:
    """
    Create a new user in the database.
    """
    new_user = User(username=username, password=password_hash, email=email)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


def read_user_by_id(session: Session, user_id: int) -> User | None:
    """
    Get a user by ID from the database.
    """
    user = session.query(User).filter(User.id == user_id).first()
    return user


def read_user_by_username_or_email(session: Session, username_or_email: str) -> User | None:
    """
    Get a user by username or email
    """
    return (
        session.query(User)
        .filter(
            ((User.username == username_or_email) | (User.email == username_or_email))
        )
        .first()
    )
