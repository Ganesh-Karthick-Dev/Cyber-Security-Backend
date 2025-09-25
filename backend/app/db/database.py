from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from ..core.config import get_settings


settings = get_settings()

# Use asyncpg for PostgreSQL
ASYNC_DATABASE_URL = str(settings.database_url).replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(ASYNC_DATABASE_URL, pool_pre_ping=True, future=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session



