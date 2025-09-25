from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1 import api_router
from .core.config import get_settings
from .db.database import Base, engine
from sqlalchemy.ext.asyncio import AsyncEngine


settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",") if o],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.on_event("startup")
async def on_startup():
    # Create tables automatically for first run (replace with Alembic in prod)
    async with engine.begin() as conn:  # type: ignore[arg-type]
        await conn.run_sync(Base.metadata.create_all)


