'use client'

import { useState, useEffect } from 'react'
import { supabase } from '@/lib/supabase'
import { apiRequestWithAuth } from '@/lib/api'

export default function InstructionsPage() {
    const [instructions, setInstructions] = useState('')
    const [loading, setLoading] = useState(true)
    const [saving, setSaving] = useState(false)
    const [error, setError] = useState('')
    const [success, setSuccess] = useState(false)
    const [lastUpdated, setLastUpdated] = useState<string>('')

    useEffect(() => {
        fetchInstructions()
    }, [])

    const fetchInstructions = async () => {
        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/instructions`)
            const data = await response.json()
            setInstructions(data.instructions)
            setLastUpdated(new Date(data.updated_at).toLocaleString())
        } catch (error: any) {
            setError('Failed to fetch instructions')
        } finally {
            setLoading(false)
        }
    }

    const handleSave = async () => {
        setSaving(true)
        setError('')
        setSuccess(false)

        try {
            const { data: { session } } = await supabase.auth.getSession()
            if (!session) throw new Error('Not authenticated')

            await apiRequestWithAuth(
                '/api/instructions',
                session.access_token,
                {
                    method: 'POST',
                    body: JSON.stringify({ instructions }),
                }
            )

            setSuccess(true)
            setTimeout(() => setSuccess(false), 3000)
            fetchInstructions()
        } catch (error: any) {
            setError(error.message)
        } finally {
            setSaving(false)
        }
    }

    if (loading) {
        return <div className="text-white">Loading...</div>
    }

    return (
        <div className="max-w-4xl">
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-white mb-2">System Instructions</h1>
                <p className="text-gray-400">Configure how your Discord bot should behave</p>
                {lastUpdated && (
                    <p className="text-gray-500 text-sm mt-1">Last updated: {lastUpdated}</p>
                )}
            </div>

            {error && (
                <div className="mb-4 bg-red-500/20 border border-red-500/50 text-red-400 px-4 py-3 rounded-lg">
                    {error}
                </div>
            )}

            {success && (
                <div className="mb-4 bg-green-500/20 border border-green-500/50 text-green-400 px-4 py-3 rounded-lg">
                    ✅ Instructions saved successfully!
                </div>
            )}

            <div className="bg-gray-900 rounded-xl border border-gray-800 p-6">
                <div className="mb-4">
                    <label htmlFor="instructions" className="block text-white font-medium mb-2">
                        Bot Instructions
                    </label>
                    <p className="text-gray-400 text-sm mb-4">
                        These instructions will guide your bot's personality and behavior. Be specific about how it should respond.
                    </p>
                </div>

                <textarea
                    id="instructions"
                    value={instructions}
                    onChange={(e) => setInstructions(e.target.value)}
                    rows={12}
                    className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500 font-mono text-sm"
                    placeholder="You are a helpful Discord assistant..."
                />

                <div className="flex items-center justify-between mt-4">
                    <p className="text-gray-400 text-sm">
                        {instructions.length} characters
                    </p>

                    <button
                        onClick={handleSave}
                        disabled={saving}
                        className="px-6 py-2 bg-purple-600 text-white rounded-lg font-medium hover:bg-purple-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {saving ? 'Saving...' : 'Save Instructions'}
                    </button>
                </div>
            </div>

            <div className="mt-6 bg-blue-500/10 border border-blue-500/30 rounded-lg p-4">
                <h3 className="text-blue-400 font-medium mb-2">💡 Tips for great instructions:</h3>
                <ul className="text-blue-300 text-sm space-y-1 list-disc list-inside">
                    <li>Define the bot's personality and tone</li>
                    <li>Specify how it should handle different types of questions</li>
                    <li>Include any domain-specific knowledge or context</li>
                    <li>Set guidelines for response length and format</li>
                </ul>
            </div>
        </div>
    )
}
