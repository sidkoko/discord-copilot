'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function HomePage() {
  const router = useRouter()

  useEffect(() => {
    router.push('/auth/login')
  }, [router])

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-950">
      <div className="text-white text-xl">Redirecting...</div>
    </div>
  )
}
