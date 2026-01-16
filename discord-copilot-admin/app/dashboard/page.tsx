'use client'

import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export default function DashboardPage() {
    const router = useRouter()

    useEffect(() => {
        // Redirect to instructions page
        router.push('/dashboard/instructions')
    }, [router])

    return (
        <div className="flex items-center justify-center min-h-[50vh]">
            <div className="text-white text-xl">Redirecting...</div>
        </div>
    )
}
