from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VisitBase(BaseModel):
    patient_id: int
    doctor_id: int
    chief_complaint: str
    diagnosis_summary: Optional[str] = None
    status: str = "PENDING"

class VisitCreate(VisitBase):
    pass

class VisitUpdate(BaseModel):
    diagnosis_summary: Optional[str] = None
    status: Optional[str] = None

class Visit(VisitBase):
    id: int
    visit_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True
