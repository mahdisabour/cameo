from fastapi import APIRouter

from app.modules.auth.routes.member import member_router

auth_router = APIRouter(prefix="/auth")

auth_router.include_router(member_router)
