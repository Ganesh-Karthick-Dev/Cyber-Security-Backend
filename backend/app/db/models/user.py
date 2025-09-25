from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from ..database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[str] = mapped_column(String(50), default="user")
    api_key: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Helper methods
    @staticmethod
    async def get_by_email(session, email: str) -> Optional["User"]:
        from sqlalchemy import select

        res = await session.execute(select(User).where(User.email == email))
        return res.scalar_one_or_none()

    @staticmethod
    async def get_by_id(session, user_id: int) -> Optional["User"]:
        from sqlalchemy import select

        res = await session.execute(select(User).where(User.id == user_id))
        return res.scalar_one_or_none()



