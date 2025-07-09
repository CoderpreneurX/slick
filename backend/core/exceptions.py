"""
This module contains the custom exceptions to be used in the application.
"""

from fastapi.responses import JSONResponse
from fastapi import Request
from typing import Union


class JSONException(Exception):
    def __init__(self, message: Union[str, dict[str, str]], status_code: int = 400):
        """
        Initialize the JSONException class.

        Args:
            message (Union[str, dict[str, str]]): The error message or error details.
            status_code (int, optional): The HTTP status code. Defaults to 400.
        """
        self.message = message
        self.status_code = status_code


# Exception handler for FastAPI
async def json_exception_handler(_: Request, exc: JSONException):
    """
    JSON exception handler for FastAPI.

    Args:
        request (Request): The request object.
        exc (JSONException): The JSONException instance.

    Returns:
        JSONResponse: The JSON response containing the error message and status code.
    """
    return JSONResponse(
        status_code=exc.status_code, content={"success": False, "message": exc.message}
    )
