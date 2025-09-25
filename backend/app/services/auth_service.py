from __future__ import annotations

from typing import Optional

from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.security import create_access_token
from ..db.models.user import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def register_user(session: AsyncSession, email: str, password: str) -> User:
    existing = await User.get_by_email(session, email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = User(email=email, hashed_password=hash_password(password))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def authenticate_user(session: AsyncSession, email: str, password: str) -> Optional[User]:
    user = await User.get_by_email(session, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def generate_token_for_user(user: User) -> str:
    return create_access_token(user.id, extra_claims={"role": user.role})



