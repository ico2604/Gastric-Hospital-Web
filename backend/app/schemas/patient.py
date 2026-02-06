from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from app.models.patient import Gender

class PatientBase(BaseModel):
    name: str
    birth_date: date
    gender: Gender
    phone: str
    patient_number: str
    blood_type: Optional[str] = None
    notes: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    blood_type: Optional[str] = None
    notes: Optional[str] = None

class Patient(PatientBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
