"""
Main module for the FastAPI application.
"""

from typing import cast

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.types import ExceptionHandler

from core.exceptions import JSONException, json_exception_handler
from core.router import router as core_router

app = FastAPI()

app.add_exception_handler(JSONException, cast(ExceptionHandler, json_exception_handler))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=core_router)
