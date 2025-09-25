from functools import lru_cache
from pydantic import BaseSettings, AnyUrl, Field


class Settings(BaseSettings):
    app_name: str = "CyberGuide Backend"
    environment: str = Field("development", env="ENVIRONMENT")
    debug: bool = Field(True, env="DEBUG")

    secret_key: str = Field(..., env="SECRET_KEY")
    access_token_expire_minutes: int = Field(60 * 24, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    algorithm: str = Field("HS256", env="JWT_ALGORITHM")

    database_url: AnyUrl = Field(..., env="DATABASE_URL")

    cors_origins: str = Field("*", env="CORS_ORIGINS")

    stripe_secret_key: str | None = Field(None, env="STRIPE_SECRET_KEY")
    stripe_publishable_key: str | None = Field(None, env="STRIPE_PUBLISHABLE_KEY")
    redis_url: str | None = Field(None, env="REDIS_URL")
    openai_api_key: str | None = Field(None, env="OPENAI_API_KEY")
    docker_host: str | None = Field(None, env="DOCKER_HOST")

    class Config:
        case_sensitive = False
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]



