from fastapi import APIRouter

from .endpoints import auth, sites, scans, plans, contact, subscriptions, ai


api_router = APIRouter(prefix="/v1")
api_router.include_router(auth.router)
api_router.include_router(sites.router)
api_router.include_router(scans.router)
api_router.include_router(plans.router)
api_router.include_router(contact.router)
api_router.include_router(subscriptions.router)
api_router.include_router(ai.router)


