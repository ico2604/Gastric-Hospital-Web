"""
API v1 Router
모든 API 엔드포인트를 통합 관리
"""

from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, ai, clinical, visits, patients, diagnoses, users

api_router = APIRouter()

# 인증
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# AI 진단
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])

# 통합 진료 워크플로우
api_router.include_router(clinical.router, prefix="/clinical", tags=["clinical"])

# 사용자 관리
api_router.include_router(users.router, prefix="/users", tags=["users"])

# 환자 관리
api_router.include_router(patients.router, prefix="/patients", tags=["patients"])

# 진료 기록 관리
api_router.include_router(visits.router, prefix="/visits", tags=["visits"])

# 진단 결과 관리
api_router.include_router(diagnoses.router, prefix="/diagnoses", tags=["diagnoses"])
