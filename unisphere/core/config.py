from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool
    HOST: str
    PORT: int
    ENVIRONMENT: str
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    USE_MOCK: bool = False
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5 * 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60
    MAX_FILE_SIZE: int = 5 * 1024 * 1024
    UPLOAD_DIR: str = "uploads"

    model_config = {
        "case_sensitive": False,
        "validate_assignment": True,
        "extra": "allow",
    }


def get_settings() -> Settings:
    return Settings()
