from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    """JWT Token schema"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token payload data"""
    username: Optional[str] = None


class UserLogin(BaseModel):
    """User login request schema"""
    username: str
    password: str


class UserRegister(BaseModel):
    """User registration request schema"""
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None