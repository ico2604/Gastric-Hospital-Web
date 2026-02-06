/**
 * 로딩 스피너 컴포넌트
 * 데이터 로딩 중 표시
 */

export default function LoadingSpinner() {
  return (
    <div className="flex justify-center items-center py-12">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>
  );
}
