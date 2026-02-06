/**
 * 전역 타입 정의
 */

// 사용자
export interface User {
  id: number
  email: string
  username: string
  full_name: string
  role: 'ADMIN' | 'DOCTOR' | 'NURSE'
  is_active: boolean
  is_superuser: boolean
  created_at: string
}

// 환자
export interface Patient {
  id: number
  name: string
  birth_date: string
  gender: 'MALE' | 'FEMALE'
  phone: string
  patient_number: string
  blood_type?: string
  notes?: string
  created_at: string
  updated_at?: string
}

// 진료 기록
export interface Visit {
  id: number
  visit_date: string
  patient: {
    id: number
    name: string
    patient_number: string
  }
  doctor: {
    id: number
    full_name: string
    username: string
  }
  chief_complaint: string
  diagnosis_summary?: string
  status: 'PENDING' | 'COMPLETED'
  created_at: string
}

// 진단 결과
export interface Diagnosis {
  id: number
  visit_id: number
  prediction: string
  prediction_kr: string
  confidence: number
  probabilities_kr: Record<string, number>
  tumor_ratio: number
  stroma_ratio: number
  normal_ratio: number
  immune_ratio: number
  background_ratio: number
  model_type: string
  processing_time: number
  is_reviewed: number
  created_at: string
}

// 통합 진료 결과
export interface ClinicalDiagnosisResult {
  visit: {
    id: number
    visit_date: string
    patient_name: string
    patient_number: string
    chief_complaint: string
    status: string
  }
  diagnosis: {
    id: number
    prediction: string
    prediction_kr: string
    confidence: number
    probabilities_kr: Record<string, number>
  }
  segmentation: {
    image_base64: string
    ratios: {
      tumor: number
      stroma: number
      normal: number
      immune: number
      background: number
    }
    class_colors: Record<string, string>
  }
  processing_time: number
}

// 통계
export interface Stats {
  total_visits: number
  completed_visits: number
  pending_visits: number
  total_patients: number
  cancer_type_distribution: Record<string, number>
}
