# 위암 진단 병원 관리 시스템 (Full-Stack)

위암 세포 현미경 이미지를 AI로 분석하여 진단하는 병원 관리 시스템!

## 주요 기능

- JWT 인증 및 권한 관리
- 환자 관리 (등록, 조회, 수정)
- AI 진단 (이미지 업로드 → 분류 + 세그멘테이션)
- 진료 내역 관리
- 대시보드 및 통계

## 기술 스택

**백엔드**: FastAPI + MySQL + PyTorch
**프론트엔드**: Next.js 13+ + TypeScript + Tailwind CSS

## 빠른 시작

### 백엔드 실행
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload

### 프론트엔드 실행
cd frontend
npm install
npm run dev

## 테스트 계정

- 관리자: admin / admin123
- 의사: doctor1 / doctor123

## API 문서

http://localhost:8000/api/v1/docs

상세 내용은 각 폴더의 README.md를 참고하세요.

- 추가 진행중 : 26.02.05(목) ~ 26.02.09(월)