from fastapi import APIRouter, Depends, HTTPException, status

from ....db.database import get_session
from ....db.schemas import Token, UserCreate, UserLogin, UserOut
from ....services.auth_service import authenticate_user, generate_token_for_user, register_user
from ....core.dependencies import get_current_user


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=201)
async def register(payload: UserCreate, session=Depends(get_session)):
    user = await register_user(session, payload.email, payload.password)
    return user


@router.post("/login", response_model=Token)
async def login(payload: UserLogin, session=Depends(get_session)):
    user = await authenticate_user(session, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = generate_token_for_user(user)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
async def me(user=Depends(get_current_user)):
    return user


@router.post("/refresh", response_model=Token)
async def refresh(user=Depends(get_current_user)):
    token = generate_token_for_user(user)
    return {"access_token": token, "token_type": "bearer"}


