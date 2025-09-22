from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.security import verify_password, create_access_token, verify_token
from app.utils.responses import APIResponse
from app.schemas.auth import Token, UserLogin

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login endpoint - similar to Express.js POST /auth/login
    Returns JWT token for authentication
    """
    # Demo user for testing (in real app, check against database)
    demo_user = {
        "username": "admin",
        "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "secret"
        "email": "admin@example.com"
    }
    
    if form_data.username != demo_user["username"]:
        return APIResponse.error(
            message="Incorrect username or password",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    if not verify_password(form_data.password, demo_user["password"]):
        return APIResponse.error(
            message="Incorrect username or password",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    access_token = create_access_token(data={"sub": demo_user["username"]})
    
    return APIResponse.success(
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "username": demo_user["username"],
                "email": demo_user["email"]
            }
        },
        message="Login successful"
    )


@router.post("/register")
async def register():
    """Register new user endpoint"""
    return APIResponse.error(
        message="Registration not implemented yet",
        status_code=status.HTTP_501_NOT_IMPLEMENTED
    )


@router.get("/me")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Get current user info - similar to Express.js middleware req.user
    Protected route that requires authentication
    """
    payload = verify_token(token)
    if payload is None:
        return APIResponse.unauthorized("Invalid token")
    
    username = payload.get("sub")
    if username is None:
        return APIResponse.unauthorized("Invalid token")
    
    # In real app, fetch user from database
    user_data = {
        "username": username,
        "email": "admin@example.com",
        "role": "admin"
    }
    
    return APIResponse.success(
        data=user_data,
        message="User retrieved successfully"
    )