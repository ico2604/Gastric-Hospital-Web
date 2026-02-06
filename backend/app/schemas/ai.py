from pydantic import BaseModel
from typing import Dict, List, Optional

class PredictionResponse(BaseModel):
    prediction: str
    prediction_kr: str
    confidence: float
    probabilities: Dict[str, float]
    probabilities_kr: Dict[str, float]
    raw_logits: List[float]
    processing_time: float
    model_info: Dict[str, str]
