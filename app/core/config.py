from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    # Application Configuration
    app_name: str = "Cyber Security Backend"
    app_version: str = "1.0.0"
    debug: bool = True
    environment: str = "development"
    
    # Database Configuration
    database_url: str = "postgresql://username:password@localhost:5432/cybersecurity_db"
    database_test_url: Optional[str] = None
    
    # Redis Configuration
    redis_url: str = "redis://localhost:6379/0"
    
    # JWT Configuration
    secret_key: str = "your-super-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS Configuration
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()