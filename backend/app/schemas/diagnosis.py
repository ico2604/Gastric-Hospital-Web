from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime

class DiagnosisBase(BaseModel):
    visit_id: int
    prediction: str
    prediction_kr: str
    confidence: float
    probabilities: Dict[str, float]
    probabilities_kr: Dict[str, float]
    raw_logits: Optional[List[float]] = None

class DiagnosisCreate(DiagnosisBase):
    model_type: Optional[str] = "ResNet50"
    processing_time: Optional[float] = None
    device: Optional[str] = "cuda"

class Diagnosis(DiagnosisBase):
    id: int
    model_type: str
    processing_time: Optional[float] = None
    device: Optional[str] = None
    is_reviewed: int
    reviewed_by_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
