/**
 * 진료 내역 페이지
 * 진료 내역 목록 조회 및 상세 보기
 */

'use client';

import { useState, useEffect } from 'react';
import api from '@/lib/api';
import Navbar from '@/components/Navbar';
import LoadingSpinner from '@/components/LoadingSpinner';
import ErrorMessage from '@/components/ErrorMessage';

interface Visit {
  id: number;
  patient_id: number;
  patient_name: string;
  doctor_id: number;
  doctor_name: string;
  visit_date: string;
  chief_complaint: string;
  diagnosis?: {
    id: number;
    disease_class: string;
    disease_class_kr: string;
    confidence: number;
    ai_analysis: any;
  };
}

export default function VisitsPage() {
  const [visits, setVisits] = useState<Visit[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedVisit, setSelectedVisit] = useState<Visit | null>(null);

  // 진료 내역 조회
  useEffect(() => {
    fetchVisits();
  }, []);

  const fetchVisits = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await api.getVisits();
      setVisits(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || '진료 내역을 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">진료 내역</h1>

          {/* 에러 메시지 */}
          {error && <ErrorMessage message={error} onRetry={fetchVisits} />}

          {/* 로딩 */}
          {loading && <LoadingSpinner />}

          {/* 진료 내역 목록 */}
          {!loading && !error && (
            <div className="bg-white shadow-md rounded-lg overflow-hidden">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      진료 ID
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      환자명
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      담당의
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      진료일
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      주소
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      진단 결과
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      상세
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {visits.map((visit) => (
                    <tr key={visit.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        #{visit.id}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {visit.patient_name}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {visit.doctor_name}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(visit.visit_date).toLocaleString('ko-KR')}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-500">
                        {visit.chief_complaint || '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        {visit.diagnosis ? (
                          <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                            {visit.diagnosis.disease_class_kr}
                          </span>
                        ) : (
                          <span className="text-gray-400">미진단</span>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <button
                          onClick={() => setSelectedVisit(visit)}
                          className="text-blue-600 hover:text-blue-900"
                        >
                          상세보기
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {visits.length === 0 && (
                <div className="text-center py-12">
                  <p className="text-gray-500">진료 내역이 없습니다.</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* 상세 보기 모달 */}
      {selectedVisit && (
        <div className="fixed z-10 inset-0 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen px-4">
            <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>

            <div className="bg-white rounded-lg overflow-hidden shadow-xl transform transition-all sm:max-w-2xl sm:w-full">
              <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  진료 내역 상세 (#{selectedVisit.id})
                </h3>

                <div className="space-y-4">
                  {/* 기본 정보 */}
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-gray-500">환자명</p>
                      <p className="font-semibold">{selectedVisit.patient_name}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">담당의</p>
                      <p className="font-semibold">{selectedVisit.doctor_name}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">진료일</p>
                      <p className="font-semibold">
                        {new Date(selectedVisit.visit_date).toLocaleString('ko-KR')}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">주소</p>
                      <p className="font-semibold">{selectedVisit.chief_complaint || '-'}</p>
                    </div>
                  </div>

                  {/* 진단 결과 */}
                  {selectedVisit.diagnosis && (
                    <div className="border-t pt-4">
                      <h4 className="font-semibold text-gray-900 mb-2">AI 진단 결과</h4>
                      
                      <div className="bg-blue-50 p-4 rounded-lg">
                        <p className="text-sm text-gray-600">진단명</p>
                        <p className="text-xl font-bold text-blue-900">
                          {selectedVisit.diagnosis.disease_class_kr}
                        </p>
                        <p className="text-sm text-gray-500 mt-1">
                          ({selectedVisit.diagnosis.disease_class})
                        </p>
                        
                        <div className="mt-3">
                          <div className="flex justify-between text-sm mb-1">
                            <span>신뢰도</span>
                            <span className="font-bold text-blue-600">
                              {(selectedVisit.diagnosis.confidence * 100).toFixed(2)}%
                            </span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-blue-600 h-2 rounded-full"
                              style={{ width: `${selectedVisit.diagnosis.confidence * 100}%` }}
                            ></div>
                          </div>
                        </div>
                      </div>

                      {/* AI 분석 상세 */}
                      {selectedVisit.diagnosis.ai_analysis && (
                        <div className="mt-4">
                          <p className="text-sm font-medium text-gray-700 mb-2">
                            클래스별 확률
                          </p>
                          <div className="space-y-2">
                            {Object.entries(
                              selectedVisit.diagnosis.ai_analysis.probabilities_kr || {}
                            ).map(([cls, prob]) => (
                              <div key={cls} className="flex justify-between text-sm">
                                <span>{cls}</span>
                                <span className="font-medium">
                                  {((prob as number) * 100).toFixed(2)}%
                                </span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>

              <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                <button
                  onClick={() => setSelectedVisit(null)}
                  className="w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none sm:w-auto sm:text-sm"
                >
                  닫기
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
