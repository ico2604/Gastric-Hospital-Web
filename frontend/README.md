# 위암 진단 시스템 - 프론트엔드

Next.js 13+ 기반 위암 진단 병원 관리 시스템 프론트엔드

## 기능

- ✅ 로그인 / JWT 인증
- ✅ 대시보드 (통계)
- ✅ 환자 관리 (등록, 조회, 수정)
- ✅ AI 진단 (이미지 업로드, 진단 결과 표시)
- ✅ 진료 내역 (목록, 상세 조회)
- ✅ 반응형 UI (Tailwind CSS)

## 기술 스택

- **Framework**: Next.js 13+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **State Management**: React Hooks

## 설치 방법

```bash
# 의존성 설치
npm install

# 환경 변수 설정
cp .env.example .env.local

# 개발 서버 실행
npm run dev
```

## 환경 변수

`.env.local` 파일에 다음 내용을 설정하세요:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## 테스트 계정

### 관리자
- **ID**: admin
- **비밀번호**: admin123

### 의사
- **ID**: doctor1
- **비밀번호**: doctor123

## 페이지 구조

```
/                    # 홈 (자동 리다이렉트)
/login               # 로그인
/dashboard           # 대시보드
/patients            # 환자 관리
/clinical            # AI 진단
/visits              # 진료 내역
```

## 주요 컴포넌트

- `Navbar`: 네비게이션 바
- `LoadingSpinner`: 로딩 표시
- `ErrorMessage`: 에러 메시지 표시

## API 연동

`src/lib/api.ts`에서 백엔드 API와 통신:

```typescript
import api from '@/lib/api';

// 예시: 환자 목록 조회
const patients = await api.getPatients();

// 예시: AI 진단
const formData = new FormData();
formData.append('patient_id', '1');
formData.append('image', imageFile);
const result = await api.diagnose(formData);
```

## 개발 명령어

```bash
# 개발 서버
npm run dev

# 빌드
npm run build

# 프로덕션 서버
npm start

# 린트
npm run lint
```

## 브라우저 지원

- Chrome (최신)
- Firefox (최신)
- Safari (최신)
- Edge (최신)

## 문의

문제가 발생하면 백엔드 서버가 실행 중인지 확인하세요:

```bash
# 백엔드 서버 확인
curl http://localhost:8000/health
```
