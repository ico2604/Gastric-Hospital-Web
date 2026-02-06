/**
 * AI 진단 페이지
 * 환자 선택, 이미지 업로드, AI 진단 실행 및 결과 표시
 */

'use client';

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import api from '@/lib/api';
import Navbar from '@/components/Navbar';
import LoadingSpinner from '@/components/LoadingSpinner';
import ErrorMessage from '@/components/ErrorMessage';

interface Patient {
  id: number;
  patient_id: string;
  name: string;
}

interface DiagnosisResult {
  visit_id: number;
  diagnosis_id: number;
  patient_name: string;
  prediction: string;
  prediction_kr: string;
  confidence: number;
  probabilities_kr: { [key: string]: number };
  segmentation_image?: string;
  processing_time: number;
}

export default function ClinicalPage() {
  const searchParams = useSearchParams();
  const preSelectedPatientId = searchParams.get('patient_id');

  const [patients, setPatients] = useState<Patient[]>([]);
  const [selectedPatientId, setSelectedPatientId] = useState('');
  const [chiefComplaint, setChiefComplaint] = useState('');
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<DiagnosisResult | null>(null);

  // 환자 목록 조회
  useEffect(() => {
    fetchPatients();
  }, []);

  // URL 파라미터로 환자가 지정된 경우 선택
  useEffect(() => {
    if (preSelectedPatientId) {
      setSelectedPatientId(preSelectedPatientId);
    }
  }, [preSelectedPatientId]);

  const fetchPatients = async () => {
    try {
      const data = await api.getPatients();
      setPatients(data);
    } catch (err: any) {
      setError('환자 목록을 불러오는데 실패했습니다.');
    }
  };

  // 이미지 선택 처리
  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setImageFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  // 진단 실행
  const handleDiagnose = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedPatientId) {
      setError('환자를 선택해주세요.');
      return;
    }
    
    if (!imageFile) {
      setError('이미지를 선택해주세요.');
      return;
    }

    try {
      setLoading(true);
      setError('');
      setResult(null);

      const formData = new FormData();
      formData.append('patient_id', selectedPatientId);
      formData.append('chief_complaint', chiefComplaint);
      formData.append('image', imageFile);

      const response = await api.diagnose(formData);
      setResult(response);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'AI 진단에 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  // 새 진단 시작
  const handleReset = () => {
    setResult(null);
    setImageFile(null);
    setImagePreview('');
    setChiefComplaint('');
    setError('');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">AI 진단</h1>

          {/* 에러 메시지 */}
          {error && <ErrorMessage message={error} />}

          {/* 진단 결과가 없을 때 - 진단 폼 */}
          {!result && (
            <div className="bg-white shadow-md rounded-lg p-6">
              <form onSubmit={handleDiagnose} className="space-y-6">
                {/* 환자 선택 */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    환자 선택
                  </label>
                  <select
                    value={selectedPatientId}
                    onChange={(e) => setSelectedPatientId(e.target.value)}
                    required
                    className="block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="">환자를 선택하세요</option>
                    {patients.map((patient) => (
                      <option key={patient.id} value={patient.id}>
                        {patient.patient_id} - {patient.name}
                      </option>
                    ))}
                  </select>
                </div>

                {/* 주소 */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    주소 (선택사항)
                  </label>
                  <textarea
                    value={chiefComplaint}
                    onChange={(e) => setChiefComplaint(e.target.value)}
                    rows={3}
                    placeholder="예: 복통, 소화불량, 정기 검진 등"
                    className="block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>

                {/* 이미지 업로드 */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    세포 현미경 이미지
                  </label>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageChange}
                    required
                    className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                  />
                </div>

                {/* 이미지 미리보기 */}
                {imagePreview && (
                  <div>
                    <p className="text-sm font-medium text-gray-700 mb-2">미리보기</p>
                    <img
                      src={imagePreview}
                      alt="Preview"
                      className="max-w-md rounded-lg border border-gray-300"
                    />
                  </div>
                )}

                {/* 제출 버튼 */}
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'AI 진단 중...' : 'AI 진단 시작'}
                </button>
              </form>

              {loading && (
                <div className="mt-6">
                  <LoadingSpinner />
                  <p className="text-center text-gray-600 mt-4">
                    AI가 이미지를 분석하고 있습니다. 잠시만 기다려주세요...
                  </p>
                </div>
              )}
            </div>
          )}

          {/* 진단 결과 표시 */}
          {result && (
            <div className="space-y-6">
              {/* 기본 정보 */}
              <div className="bg-white shadow-md rounded-lg p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">진단 결과</h2>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-500">환자명</p>
                    <p className="text-lg font-semibold">{result.patient_name}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">진단 ID</p>
                    <p className="text-lg font-semibold">#{result.diagnosis_id}</p>
                  </div>
                </div>
              </div>

              {/* AI 진단 결과 */}
              <div className="bg-white shadow-md rounded-lg p-6">
                <h3 className="text-lg font-bold text-gray-900 mb-4">AI 분석 결과</h3>
                
                {/* 주 진단 */}
                <div className="bg-blue-50 border-l-4 border-blue-600 p-4 mb-4">
                  <p className="text-sm text-gray-600">진단명</p>
                  <p className="text-2xl font-bold text-blue-900 mt-1">
                    {result.prediction_kr}
                  </p>
                  <p className="text-sm text-gray-500 mt-1">({result.prediction})</p>
                </div>

                {/* 신뢰도 */}
                <div className="mb-4">
                  <div className="flex justify-between mb-1">
                    <span className="text-sm font-medium text-gray-700">신뢰도</span>
                    <span className="text-sm font-bold text-blue-600">
                      {(result.confidence * 100).toFixed(2)}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div
                      className="bg-blue-600 h-2.5 rounded-full"
                      style={{ width: `${result.confidence * 100}%` }}
                    ></div>
                  </div>
                </div>

                {/* 클래스별 확률 */}
                <div>
                  <p className="text-sm font-medium text-gray-700 mb-2">클래스별 확률</p>
                  <div className="space-y-2">
                    {Object.entries(result.probabilities_kr).map(([cls, prob]) => (
                      <div key={cls}>
                        <div className="flex justify-between text-sm mb-1">
                          <span>{cls}</span>
                          <span className="font-medium">{(prob * 100).toFixed(2)}%</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div
                            className="bg-gray-600 h-2 rounded-full"
                            style={{ width: `${prob * 100}%` }}
                          ></div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* 처리 시간 */}
                <p className="text-sm text-gray-500 mt-4">
                  처리 시간: {result.processing_time.toFixed(3)}초
                </p>
              </div>

              {/* 세그멘테이션 이미지 */}
              {result.segmentation_image && (
                <div className="bg-white shadow-md rounded-lg p-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">
                    세그멘테이션 결과
                  </h3>
                  <img
                    src={`data:image/png;base64,${result.segmentation_image}`}
                    alt="Segmentation"
                    className="w-full rounded-lg border border-gray-300"
                  />
                  <p className="text-sm text-gray-500 mt-2">
                    * 색상: 빨강(종양), 초록(기질), 파랑(정상), 노랑(면역세포)
                  </p>
                </div>
              )}

              {/* 새 진단 버튼 */}
              <button
                onClick={handleReset}
                className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-4 rounded-lg"
              >
                새 진단 시작
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
