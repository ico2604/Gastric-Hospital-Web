"""
통합 진료 워크플로우 API
환자 진료 → AI 진단 → 결과 저장을 한 번에 처리
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import tempfile
import os
import base64
from io import BytesIO
from PIL import Image

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.patient import Patient
from app.models.visit import Visit
from app.models.diagnosis import Diagnosis
from app.services.ai_service import ai_service

router = APIRouter()


@router.post("/diagnose")
async def create_clinical_diagnosis(
    patient_id: int = Form(..., description="환자 ID"),
    chief_complaint: str = Form(..., description="주 증상"),
    image: UploadFile = File(..., description="현미경 이미지"),
    # notes: Optional[str] = Form(None, description="의사 소견"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    통합 진료 워크플로우
    
    1. 환자 정보 확인
    2. 진료 기록 생성
    3. AI 진단 수행 (분류 + 세그멘테이션)
    4. 진단 결과 저장
    5. 세그멘테이션 이미지 반환
    
    - 인증 필요 (의사 권한)
    """
    print(f"patient_id: {patient_id}")
    print(f"chief_complaint: {chief_complaint}")
    print(f"image: {image}")
    print(f"current_user: {current_user}")
    # 1. 권한 체크 (의사만 가능)
    if current_user.role.value not in ["ADMIN", "DOCTOR"]:
        raise HTTPException(status_code=403, detail="의사 권한이 필요합니다.")
    
    # 2. 환자 존재 확인
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="환자를 찾을 수 없습니다.")
    
    # 3. 이미지 유효성 검사
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")
    
    # 4. 임시 파일로 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(image.filename)[1]) as tmp:
        content = await image.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        # 5. AI 진단 수행
        result = ai_service.predict(tmp_path)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result.get("message", "AI 진단 실패"))
        
        # 6. 진료 기록 생성
        visit = Visit(
            patient_id=patient_id,
            doctor_id=current_user.id,
            chief_complaint=chief_complaint,
            diagnosis_summary=f"AI 진단: {result['prediction_kr']}",
            status="COMPLETED",
            visit_date=datetime.utcnow()
        )
        db.add(visit)
        db.flush()  # visit.id 생성을 위해
        
        import json

        # 7. 진단 결과 저장
        diagnosis = Diagnosis(
            visit_id=visit.id,
            prediction=result["prediction"],
            prediction_kr=result["prediction_kr"],
            confidence=result["confidence"],
            probabilities=json.dumps(result["probabilities"]),
            probabilities_kr=json.dumps(result["probabilities_kr"]),
            raw_logits=json.dumps(result.get("raw_logits")),
            
            # MTL 세그멘테이션 정보 - ["stats"] 추가
            tumor_ratio=result["segmentation"]["stats"]["ratios"]["tumor"],
            stroma_ratio=result["segmentation"]["stats"]["ratios"]["stroma"],
            normal_ratio=result["segmentation"]["stats"]["ratios"]["normal"],
            immune_ratio=result["segmentation"]["stats"]["ratios"]["immune"],
            background_ratio=result["segmentation"]["stats"]["ratios"]["background"],
            
            model_type=result["model_info"]["model_type"],
            processing_time=result["processing_time"],
            device=result["model_info"]["device"],
            is_reviewed=0
        )
        db.add(diagnosis)
        db.commit()
        db.refresh(visit)
        db.refresh(diagnosis)
        
        # 8. 응답 구성
        response = {
            "visit": {
                "id": visit.id,
                "visit_date": visit.visit_date.isoformat(),
                "patient_name": patient.name,
                "patient_number": patient.patient_number,
                "chief_complaint": chief_complaint,
                "status": visit.status
            },
            "diagnosis": {
                "id": diagnosis.id,
                "prediction": result["prediction"],
                "prediction_kr": result["prediction_kr"],
                "confidence": result["confidence"],
                # "probabilities_kr": result["probabilities_kr"],
                "probabilities_kr": (
                    json.loads(result["probabilities_kr"]) 
                    if isinstance(result["probabilities_kr"], str) 
                    else result["probabilities_kr"]
                ),
            },
            "segmentation": {
                "image_base64": result["segmentation"]["image_base64"],
                "ratios": result["segmentation"]["stats"]["ratios"],
                "class_colors": result["segmentation"]["class_colors"]
            },
            "processing_time": result["processing_time"]
        }
        
        return response
        
    finally:
        # 9. 임시 파일 삭제
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@router.get("/stats")
def get_clinical_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    진료 통계 조회
    
    - 전체 진료 건수
    - 암 유형별 통계
    - 최근 진료 내역
    """
    
    # 전체 진료 건수
    total_visits = db.query(Visit).count()
    
    # 완료된 진료 건수
    completed_visits = db.query(Visit).filter(Visit.status == "COMPLETED").count()
    
    # 대기 중인 진료 건수
    pending_visits = db.query(Visit).filter(Visit.status == "PENDING").count()
    
    # 전체 환자 수
    total_patients = db.query(Patient).count()
    
    # 암 유형별 통계
    diagnoses = db.query(Diagnosis).all()
    cancer_stats = {}
    for diag in diagnoses:
        cancer_type = diag.prediction_kr
        cancer_stats[cancer_type] = cancer_stats.get(cancer_type, 0) + 1
    
    return {
        "total_visits": total_visits,
        "completed_visits": completed_visits,
        "pending_visits": pending_visits,
        "total_patients": total_patients,
        "cancer_type_distribution": cancer_stats
    }
