from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from fastapi import HTTPException, status
from jose import JWTError, jwt

from .config import get_settings


def create_access_token(subject: str | int, expires_delta_minutes: Optional[int] = None, extra_claims: dict[str, Any] | None = None) -> str:
    settings = get_settings()
    if expires_delta_minutes is None:
        expires_delta_minutes = settings.access_token_expire_minutes

    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta_minutes)
    to_encode: dict[str, Any] = {"sub": str(subject), "exp": expire}
    if extra_claims:
        to_encode.update(extra_claims)
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def decode_token(token: str) -> dict[str, Any]:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc



