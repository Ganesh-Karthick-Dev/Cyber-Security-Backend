from fastapi import APIRouter
from app.api.endpoints import auth, users, security_events

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(security_events.router, prefix="/security", tags=["Security Events"])