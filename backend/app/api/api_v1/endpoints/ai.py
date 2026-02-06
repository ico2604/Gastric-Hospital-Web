from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ai_service import ai_service
from app.schemas.ai import PredictionResponse
import tempfile
import os

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
async def predict_image(file: UploadFile = File(...)):
    """이미지 업로드 및 AI 예측"""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")
    
    # 임시 파일로 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        result = ai_service.predict(tmp_path)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["message"])
        return result
    finally:
        os.unlink(tmp_path)

@router.get("/model-info")
def get_model_info():
    """모델 정보 조회"""
    return {
        "model_type": "ResNet50",
        "classes": ai_service.CLASS_NAMES,
        "classes_kr": ai_service.CLASS_NAMES_KR,
        "device": str(ai_service.device),
        "model_loaded": ai_service.model is not None
    }
