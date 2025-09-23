from typing import Any, Dict, Optional
from pydantic_settings import BaseSettings
from pydantic import validator
import os
from functools import lru_cache


class Settings(BaseSettings):
    # Application
    app_name: str = "Unisphere API"
    app_version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database
    database_url: str = "postgresql://username:password@localhost/unisphere_db"
    database_test_url: Optional[str] = None
    
    # JWT
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 7  # 7 days
    
    # CORS
    allowed_hosts: list[str] = ["*"]
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:8081",  # Flutter web dev
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:8081",
    ]
    
    # File Upload
    max_file_size: int = 5 * 1024 * 1024  # 5MB
    upload_directory: str = "uploads"
    
    @validator("database_url", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return "postgresql://username:password@localhost/unisphere_db"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()