# 🚀 위암 분류 병원 관리 시스템 - 빠른 시작 가이드
## Multi-Task Learning (UNet + ResNet50) 지원


# test sub1
## 📋 필수 요구사항

- Python 3.9+
- MySQL 8.0+
- NVIDIA GPU (선택, CUDA 12.1+)
- Windows 10/11 or Linux

---

## 🔧 1단계: UV 설치

```powershell
# PowerShell에서 실행
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## 🐍 2단계: 가상환경 생성

```powershell
cd backend
uv venv --python 3.11
.\.venv\Scripts\Activate.ps1
```
# main 작업내용
---

## 📦 3단계: 패키지 설치

```powershell
# NumPy 먼저 설치
uv pip install "numpy>=1.24.0,<2.0.0"

# 기본 패키지
uv pip install fastapi==0.109.0 uvicorn[standard]==0.27.0 sqlalchemy==2.0.25 alembic==1.13.1 pymysql==1.1.0 cryptography==42.0.0 python-jose[cryptography]==3.3.0 passlib[bcrypt]==1.7.4 python-multipart==0.0.6 opencv-python-headless==4.9.0.80 "pillow>=11.0.0" albumentations==1.3.1 python-dotenv pydantic pydantic-settings email-validator

# PyTorch (GPU 버전)
uv pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu121

# PyTorch (CPU 버전) - GPU 없는 경우
# uv pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cpu
```

---

## ⚙️ 4단계: 환경 설정

```powershell
# .env 파일 생성
copy .env.example .env
notepad .env
```

**.env 수정:**
```ini
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/gastric_hospital
SECRET_KEY=your-random-secret-key-32-chars-minimum
ENCRYPTION_KEY=your-encryption-key-base64-encoded
```

---

## 🗄️ 5단계: 데이터베이스 초기화

```powershell
# MySQL 데이터베이스 생성
mysql -u root -p -e "CREATE DATABASE gastric_hospital CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 테이블 생성 및 초기 데이터 입력
python init_db.py
```

**예상 출력:**
```
============================================================
🏥 위암 분류 병원 관리 시스템 - 데이터베이스 초기화
   Multi-Task Learning (UNet + ResNet50) 지원
============================================================
📊 테이블 생성 중...
✅ 테이블 생성 완료
👥 사용자 계정 생성 중...
   ✅ 생성: 시스템 관리자 (ADMIN)
   ✅ 생성: 김의사 (DOCTOR)
   ✅ 생성: 이의사 (DOCTOR)
   ✅ 생성: 박간호사 (NURSE)
✅ 사용자 4명 생성 완료
🏥 샘플 환자 데이터 생성 중...
   ✅ 생성: 홍길동 (P2024001)
   ✅ 생성: 김영희 (P2024002)
✅ 환자 2명 생성 완료
🎉 데이터베이스 초기화 완료!
```

---

## 🤖 6단계: AI 모델 배치

```powershell
# UNet + ResNet50 모델 파일 복사
copy path\to\unet_resnet50_best.pth .

# 확인
Get-Item unet_resnet50_best.pth
```

---

## 🚀 7단계: 서버 실행

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**접속:**
- API 문서: http://localhost:8000/api/v1/docs
- Health Check: http://localhost:8000/health

---

## 🧪 8단계: API 테스트

### Health Check
```powershell
curl http://localhost:8000/health
```

### 로그인 테스트
```powershell
curl -X POST "http://localhost:8000/api/v1/auth/login" `
  -H "Content-Type: application/json" `
  -d '{\"username\":\"doctor1\",\"password\":\"doctor123\"}'
```

### AI 예측 테스트 (Multi-Task)
```powershell
curl.exe -X POST "http://localhost:8000/api/v1/ai-mtl/predict" `
  -F "file=@test_image.jpg" `
  -H "accept: application/json"
```

---

## 🔐 기본 계정

| 역할 | 아이디 | 비밀번호 |
|------|--------|----------|
| 관리자 | admin | admin123 |
| 의사1 | doctor1 | doctor123 |
| 의사2 | doctor2 | doctor123 |
| 간호사 | nurse1 | nurse123 |

---

## 🐛 문제 해결

### 1. conda 자동 활성화
```powershell
conda config --set auto_activate_base false
```

### 2. PowerShell 실행 정책
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. MySQL 연결 오류
```powershell
net start MySQL80
```

### 4. 포트 충돌
```powershell
netstat -ano | findstr :8000
taskkill /F /PID <PID>
```

---

## 📊 Multi-Task Learning 특징

### Classification (분류)
- **STDI**: 미만형 선암 (Diffuse-type)
- **STNT**: 위염 (Gastritis)
- **STIN**: 장형 선암 (Intestinal-type)
- **STMX**: 혼합형 선암 (Mixed-type)

### Segmentation (세그멘테이션)
- **Tumor**: 종양 영역
- **Stroma**: 간질 조직
- **Normal**: 정상 조직
- **Immune**: 면역세포
- **Background**: 배경

---

## 📝 다음 단계

1. 프론트엔드 설치 (`frontend/` 디렉터리)
2. Docker 배포 (`docker-compose.yml`)
3. 프로덕션 환경 설정

---

**설치 완료! 🎉**
