from fastapi import APIRouter

from .routes.group import group_router

auth_router = APIRouter(prefix="/auth")

auth_router.include_router(user_router)
