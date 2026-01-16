'use client'

import { useEffect, useState } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import { supabase } from '@/lib/supabase'
import Link from 'next/link'
import { User } from '@supabase/supabase-js'

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode
}) {
    const [user, setUser] = useState<User | null>(null)
    const [loading, setLoading] = useState(true)
    const router = useRouter()
    const pathname = usePathname()

    useEffect(() => {
        checkUser()
    }, [])

    const checkUser = async () => {
        const { data: { user } } = await supabase.auth.getUser()

        if (!user) {
            router.push('/auth/login')
            return
        }

        setUser(user)
        setLoading(false)
    }

    const handleLogout = async () => {
        await supabase.auth.signOut()
        router.push('/auth/login')
    }

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-950">
                <div className="text-white text-xl">Loading...</div>
            </div>
        )
    }

    const navItems = [
        { href: '/dashboard/instructions', label: 'System Instructions', icon: '📝' },
        { href: '/dashboard/knowledge', label: 'Knowledge Base', icon: '📚' },
        { href: '/dashboard/memory', label: 'Conversation Memory', icon: '🧠' },
        { href: '/dashboard/channels', label: 'Channels', icon: '💬' },
    ]

    return (
        <div className="min-h-screen bg-gray-950">
            {/* Sidebar */}
            <div className="fixed inset-y-0 left-0 w-64 bg-gray-900 border-r border-gray-800">
                <div className="p-6">
                    <h1 className="text-2xl font-bold text-white mb-2">Discord Copilot</h1>
                    <p className="text-gray-400 text-sm">Admin Dashboard</p>
                </div>

                <nav className="px-4 space-y-2">
                    {navItems.map((item) => {
                        const isActive = pathname === item.href
                        return (
                            <Link
                                key={item.href}
                                href={item.href}
                                className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${isActive
                                        ? 'bg-purple-600 text-white'
                                        : 'text-gray-400 hover:bg-gray-800 hover:text-white'
                                    }`}
                            >
                                <span className="text-xl">{item.icon}</span>
                                <span className="font-medium">{item.label}</span>
                            </Link>
                        )
                    })}
                </nav>

                <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-800">
                    <div className="flex items-center justify-between mb-3">
                        <div className="text-sm">
                            <p className="text-white font-medium">{user?.email}</p>
                            <p className="text-gray-400 text-xs">Admin</p>
                        </div>
                    </div>
                    <button
                        onClick={handleLogout}
                        className="w-full py-2 px-4 bg-red-600/20 text-red-400 rounded-lg hover:bg-red-600/30 transition-all text-sm font-medium"
                    >
                        Sign Out
                    </button>
                </div>
            </div>

            {/* Main Content */}
            <div className="ml-64 min-h-screen">
                <div className="p-8">
                    {children}
                </div>
            </div>
        </div>
    )
}
