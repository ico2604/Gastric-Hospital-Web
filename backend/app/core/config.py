"""
Application configuration
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # 프로젝트 정보
    PROJECT_NAME: str = "Gastric Hospital Backend"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"
    
    # 환경
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # 데이터베이스
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/gastric_hospital"
    
    # JWT 설정
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 암호화
    ENCRYPTION_KEY: str = "your-32-byte-encryption-key-here"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # 서버
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # AI 모델
    AI_MODEL_PATH: str = "unet_resnet50_best.pth"
    AI_DEVICE: str = "cuda"  # cuda or cpu
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
