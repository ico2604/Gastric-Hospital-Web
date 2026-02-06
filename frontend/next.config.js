/** @type {import('next').NextConfig} */
const nextConfig = {
  // API 백엔드 프록시 설정
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*'
      }
    ]
  }
}

module.exports = nextConfig
