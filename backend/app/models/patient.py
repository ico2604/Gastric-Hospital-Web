"""
Patient Model (환자 정보 - 암호화 저장)
"""

from sqlalchemy import Column, Integer, String, Date, DateTime, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.models.base import Base


class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 기본 정보
    name = Column(String(100), nullable=False, index=True)
    birth_date = Column(Date, nullable=False)
    gender = Column(SQLEnum(Gender), nullable=False)
    
    # 개인정보 (암호화 저장)
    phone = Column(Text)  # 암호화된 전화번호
    ssn = Column(Text)  # 암호화된 주민등록번호
    address = Column(Text)  # 암호화된 주소
    
    # 의료 정보
    blood_type = Column(String(10))
    allergies = Column(Text)  # 알레르기
    medical_history = Column(Text)  # 과거 병력
    
    # 메타 정보
    patient_number = Column(String(50), unique=True, index=True)  # 환자 번호
    notes = Column(Text)  # 추가 메모
    
    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    visits = relationship("Visit", back_populates="patient", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Patient(id={self.id}, name={self.name}, number={self.patient_number})>"
