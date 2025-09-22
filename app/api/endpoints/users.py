from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from app.api.endpoints.auth import oauth2_scheme
from app.utils.responses import APIResponse
from app.schemas.user import UserResponse, UserCreate

router = APIRouter()


async def get_current_user_dependency(token: str = Depends(oauth2_scheme)):
    """Dependency to get current user from token"""
    from app.core.security import verify_token
    payload = verify_token(token)
    if payload is None:
        return None
    return payload.get("sub")


@router.get("/")
async def get_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to return"),
    current_user: str = Depends(get_current_user_dependency)
):
    """
    Get all users with pagination - similar to Express.js GET /users
    Protected route
    """
    if current_user is None:
        return APIResponse.unauthorized()
    
    # Demo data (in real app, fetch from database)
    demo_users = [
        {"id": 1, "username": "admin", "email": "admin@example.com", "role": "admin"},
        {"id": 2, "username": "user1", "email": "user1@example.com", "role": "user"},
        {"id": 3, "username": "user2", "email": "user2@example.com", "role": "user"},
    ]
    
    # Apply pagination
    paginated_users = demo_users[skip:skip + limit]
    
    return APIResponse.success(
        data={
            "users": paginated_users,
            "total": len(demo_users),
            "skip": skip,
            "limit": limit
        },
        message="Users retrieved successfully"
    )


@router.get("/{user_id}")
async def get_user(
    user_id: int,
    current_user: str = Depends(get_current_user_dependency)
):
    """
    Get user by ID - similar to Express.js GET /users/:id
    Protected route
    """
    if current_user is None:
        return APIResponse.unauthorized()
    
    # Demo user lookup (in real app, query database)
    if user_id == 1:
        user_data = {"id": 1, "username": "admin", "email": "admin@example.com", "role": "admin"}
        return APIResponse.success(
            data=user_data,
            message="User found"
        )
    
    return APIResponse.not_found("User not found")


@router.post("/")
async def create_user(
    current_user: str = Depends(get_current_user_dependency)
):
    """
    Create new user - similar to Express.js POST /users
    Protected route (admin only)
    """
    if current_user is None:
        return APIResponse.unauthorized()
    
    return APIResponse.error(
        message="User creation not implemented yet",
        status_code=501
    )


@router.put("/{user_id}")
async def update_user(
    user_id: int,
    current_user: str = Depends(get_current_user_dependency)
):
    """
    Update user - similar to Express.js PUT /users/:id
    Protected route
    """
    if current_user is None:
        return APIResponse.unauthorized()
    
    return APIResponse.error(
        message="User update not implemented yet",
        status_code=501
    )


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: str = Depends(get_current_user_dependency)
):
    """
    Delete user - similar to Express.js DELETE /users/:id
    Protected route (admin only)
    """
    if current_user is None:
        return APIResponse.unauthorized()
    
    return APIResponse.error(
        message="User deletion not implemented yet",
        status_code=501
    )