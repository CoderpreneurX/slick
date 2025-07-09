from fastapi import APIRouter

from apps.auth.routes import router as auth_router

router = APIRouter(prefix="/api")

router.include_router(router=auth_router)
