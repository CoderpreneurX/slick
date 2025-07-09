"""
This module contains the application settings.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings.
    """

    # Database
    DATABASE_URL: str = Field(default="sqlite:///./test.db")

    # Security
    ACCESS_TOKEN_SECRET_KEY: str = Field(default="super-secret-key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=15)
    REFRESH_TOKEN_SECRET_KEY: str = Field(default="super-secret-key")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)
    JWT_ALGORITHM: str = Field(default="HS256")

    # Other app-level configs
    DEBUG: bool = Field(default=True)

    class Config:
        """
        Configuration for the application settings.
        """

        env_file = ".env"  # Load variables from a .env file
        env_file_encoding = "utf-8"


# Use lru_cache to avoid reloading settings multiple times
@lru_cache()
def get_settings() -> Settings:
    """Get the application settings."""
    return Settings()
