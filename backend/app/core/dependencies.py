from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from ..db.database import get_session
from ..db.models.user import User
from .security import decode_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session=Depends(get_session)) -> User:
    payload = decode_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    user = await User.get_by_id(session, int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


async def get_api_key(x_api_key: Annotated[str | None, Header(alias="X-API-Key")]):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="X-API-Key required")
    return x_api_key



