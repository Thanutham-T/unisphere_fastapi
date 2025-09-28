from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Unisphere API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    HOST: str = "localhost"
    PORT: int = 8000
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "postgresql://user:password@localhost/db"
    REDIS_URL: str = "redis://localhost:6379"
    SECRET_KEY: str = "your-secret-key-here"
    JWT_SECRET_KEY: str = "your-jwt-secret-key-here"
    JWT_ALGORITHM: str = "HS256"
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
