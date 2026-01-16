'use client'

import { useState, useEffect } from 'react'
import { supabase } from '@/lib/supabase'
import { apiRequestWithAuth } from '@/lib/api'

interface Memory {
    id: string
    summary: string
    last_updated: string
    message_count: number
}

export default function MemoryPage() {
    const [memory, setMemory] = useState<Memory | null>(null)
    const [loading, setLoading] = useState(true)
    const [resetting, setResetting] = useState(false)
    const [error, setError] = useState('')
    const [success, setSuccess] = useState(false)

    useEffect(() => {
        fetchMemory()
    }, [])

    const fetchMemory = async () => {
        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/memory`)
            const data = await response.json()
            setMemory(data)
        } catch (error: any) {
            setError('Failed to fetch memory')
        } finally {
            setLoading(false)
        }
    }

    const handleReset = async () => {
        if (!confirm('Are you sure you want to reset the conversation memory? This cannot be undone.')) {
            return
        }

        setResetting(true)
        setError('')
        setSuccess(false)

        try {
            const { data: { session } } = await supabase.auth.getSession()
            if (!session) throw new Error('Not authenticated')

            await apiRequestWithAuth(
                '/api/memory',
                session.access_token,
                { method: 'DELETE' }
            )

            setSuccess(true)
            setTimeout(() => setSuccess(false), 3000)
            fetchMemory()
        } catch (error: any) {
            setError(error.message)
        } finally {
            setResetting(false)
        }
    }

    if (loading) {
        return <div className="text-white">Loading...</div>
    }

    return (
        <div className="max-w-4xl">
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-white mb-2">Conversation Memory</h1>
                <p className="text-gray-400">View and manage your bot's conversation context</p>
            </div>

            {error && (
                <div className="mb-4 bg-red-500/20 border border-red-500/50 text-red-400 px-4 py-3 rounded-lg">
                    {error}
                </div>
            )}

            {success && (
                <div className="mb-4 bg-green-500/20 border border-green-500/50 text-green-400 px-4 py-3 rounded-lg">
                    ✅ Memory reset successfully!
                </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div className="bg-gray-900 rounded-xl border border-gray-800 p-6">
                    <div className="flex items-center gap-3 mb-2">
                        <span className="text-3xl">💬</span>
                        <div>
                            <p className="text-gray-400 text-sm">Message Count</p>
                            <p className="text-white text-2xl font-bold">{memory?.message_count || 0}</p>
                        </div>
                    </div>
                </div>

                <div className="bg-gray-900 rounded-xl border border-gray-800 p-6">
                    <div className="flex items-center gap-3 mb-2">
                        <span className="text-3xl">🕒</span>
                        <div>
                            <p className="text-gray-400 text-sm">Last Updated</p>
                            <p className="text-white text-lg font-medium">
                                {memory ? new Date(memory.last_updated).toLocaleString() : 'Never'}
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <div className="bg-gray-900 rounded-xl border border-gray-800 p-6">
                <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-3">
                        <h2 className="text-white text-xl font-semibold">Current Summary</h2>
                        <button
                            onClick={() => { setLoading(true); fetchMemory(); }}
                            disabled={loading}
                            className="p-2 text-gray-400 hover:text-white hover:bg-gray-700 rounded-lg transition-all disabled:opacity-50"
                            title="Refresh"
                        >
                            <svg className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                            </svg>
                        </button>
                    </div>
                    <button
                        onClick={handleReset}
                        disabled={resetting}
                        className="px-4 py-2 bg-red-600/20 text-red-400 border border-red-600/30 rounded-lg hover:bg-red-600/30 transition-all disabled:opacity-50 disabled:cursor-not-allowed font-medium"
                    >
                        {resetting ? 'Resetting...' : '🗑️ Reset Memory'}
                    </button>
                </div>

                <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
                    <p className="text-gray-300 whitespace-pre-wrap">
                        {memory?.summary || 'No conversation history yet.'}
                    </p>
                </div>
            </div>

            <div className="mt-6 bg-blue-500/10 border border-blue-500/30 rounded-lg p-4">
                <h3 className="text-blue-400 font-medium mb-2">ℹ️ About Conversation Memory</h3>
                <ul className="text-blue-300 text-sm space-y-1 list-disc list-inside">
                    <li>The bot maintains a rolling summary of conversations to provide context</li>
                    <li>This helps the bot remember previous interactions and provide better answers</li>
                    <li>Reset memory when starting a new topic or if the bot seems confused</li>
                    <li>Memory is automatically updated after each bot interaction</li>
                </ul>
            </div>
        </div>
    )
}
