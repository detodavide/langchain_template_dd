from fastapi import APIRouter
from .user_route import router as user_router
from .auth.auth_route import router as auth_router

router = APIRouter()

router.include_router(user_router, prefix="/users", tags=["users"])
router.include_router(auth_router, prefix="", tags=["auth_token"])
