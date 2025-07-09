"""
This module contains the Routes for the auth module.
"""

from fastapi import APIRouter

from apps.auth.endpoints import (
    get_user_endpoint,
    login_user_endpoint,
    refresh_access_token_endpoint,
    register_user_endpoint,
)

router = APIRouter(prefix="/auth", tags=["Authentication & Authorization"])

router.add_api_route(
    path="/register", endpoint=register_user_endpoint, methods=["POST"]
)
router.add_api_route(path="/login", endpoint=login_user_endpoint, methods=["POST"])
router.add_api_route(path="/me", endpoint=get_user_endpoint, methods=["GET"])
router.add_api_route(
    path="/refresh-access-token",
    endpoint=refresh_access_token_endpoint,
    methods=["GET"],
)
