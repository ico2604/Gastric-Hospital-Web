'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import api from '@/lib/api'

export default function AuthenticatedLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('access_token')
      console.log("token:"+token)
      // 1. 토큰 자체가 없으면 즉시 로그인으로 리다이렉트
      if (!token) {
        // router.push('/login')
        return
      }

      try {
        // 2. /me 호출: 토큰의 유효성을 검증하고 최신 유저 정보를 가져옴
        const userData = await api.getCurrentUser()
        console.log("user:"+JSON.stringify(userData))
        // 3. 새로고침 시에도 유저 정보를 복구할 수 있도록 저장
        localStorage.setItem('user', JSON.stringify(userData))
        
        setIsLoading(false) // 인증 성공 시 화면을 보여줌
      } catch (err) {
        // 4. 토큰이 만료되었거나 서버 에러인 경우 세션 초기화 후 쫓아냄
        console.error("인증 실패:", err)
        localStorage.removeItem('access_token')
        localStorage.removeItem('user')
        //router.push('/login')
      }
    }

    checkAuth()
  }, [router])

  // 인증 확인 중에는 로딩 화면을 보여주어 데이터 노출을 방지합니다.
  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-white">
        <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="mt-4 text-gray-600 font-medium">사용자 정보를 확인 중입니다...</p>
      </div>
    )
  }

  // 인증 성공 시 하위 페이지(dashboard 등)를 렌더링
  return <>{children}</>
}