"""
User Model (사용자: 관리자, 의사, 간호사)
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.models.base import Base


class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    DOCTOR = "DOCTOR"
    NURSE = "NURSE"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # 프로필
    full_name = Column(String(100))
    role = Column(SQLEnum(UserRole), default=UserRole.DOCTOR, nullable=False)
    
    # 상태
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"
