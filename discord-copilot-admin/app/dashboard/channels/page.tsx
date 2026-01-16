'use client'

import { useState, useEffect } from 'react'
import { supabase } from '@/lib/supabase'
import { apiRequestWithAuth } from '@/lib/api'

interface Channel {
    id: string
    channel_id: string
    channel_name: string | null
    added_at: string
}

export default function ChannelsPage() {
    const [channels, setChannels] = useState<Channel[]>([])
    const [loading, setLoading] = useState(true)
    const [adding, setAdding] = useState(false)
    const [channelId, setChannelId] = useState('')
    const [channelName, setChannelName] = useState('')
    const [error, setError] = useState('')
    const [success, setSuccess] = useState('')

    useEffect(() => {
        fetchChannels()
    }, [])

    const fetchChannels = async () => {
        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/channels`)
            const data = await response.json()
            setChannels(data)
        } catch (error: any) {
            setError('Failed to fetch channels')
        } finally {
            setLoading(false)
        }
    }

    const handleAdd = async (e: React.FormEvent) => {
        e.preventDefault()
        setAdding(true)
        setError('')
        setSuccess('')

        try {
            const { data: { session } } = await supabase.auth.getSession()
            if (!session) throw new Error('Not authenticated')

            await apiRequestWithAuth(
                '/api/channels',
                session.access_token,
                {
                    method: 'POST',
                    body: JSON.stringify({
                        channel_id: channelId,
                        channel_name: channelName || null,
                    }),
                }
            )

            setSuccess('✅ Channel added successfully!')
            setChannelId('')
            setChannelName('')
            fetchChannels()
        } catch (error: any) {
            setError(error.message)
        } finally {
            setAdding(false)
        }
    }

    const handleRemove = async (channel: Channel) => {
        if (!confirm(`Remove "${channel.channel_name || channel.channel_id}" from allow-list?`)) {
            return
        }

        try {
            const { data: { session } } = await supabase.auth.getSession()
            if (!session) return

            await apiRequestWithAuth(
                `/api/channels/${channel.channel_id}`,
                session.access_token,
                { method: 'DELETE' }
            )

            setSuccess('✅ Channel removed successfully!')
            fetchChannels()
        } catch (error: any) {
            setError(`Failed to remove channel: ${error.message}`)
        }
    }

    return (
        <div className="max-w-4xl">
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-white mb-2">Channel Configuration</h1>
                <p className="text-gray-400">Manage which Discord channels the bot can respond in</p>
            </div>

            {error && (
                <div className="mb-4 bg-red-500/20 border border-red-500/50 text-red-400 px-4 py-3 rounded-lg">
                    {error}
                </div>
            )}

            {success && (
                <div className="mb-4 bg-green-500/20 border border-green-500/50 text-green-400 px-4 py-3 rounded-lg">
                    {success}
                </div>
            )}

            {/* Add Channel Form */}
            <div className="bg-gray-900 rounded-xl border border-gray-800 p-6 mb-8">
                <h2 className="text-white text-xl font-semibold mb-4">Add Channel</h2>

                <form onSubmit={handleAdd} className="space-y-4">
                    <div>
                        <label htmlFor="channelId" className="block text-white font-medium mb-2">
                            Channel ID *
                        </label>
                        <input
                            id="channelId"
                            type="text"
                            value={channelId}
                            onChange={(e) => setChannelId(e.target.value)}
                            required
                            className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500"
                            placeholder="123456789012345678"
                        />
                    </div>

                    <div>
                        <label htmlFor="channelName" className="block text-white font-medium mb-2">
                            Channel Name (optional)
                        </label>
                        <input
                            id="channelName"
                            type="text"
                            value={channelName}
                            onChange={(e) => setChannelName(e.target.value)}
                            className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500"
                            placeholder="general"
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={adding}
                        className="w-full py-3 px-4 bg-purple-600 text-white rounded-lg font-medium hover:bg-purple-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {adding ? 'Adding...' : 'Add Channel'}
                    </button>
                </form>
            </div>

            {/* How to get Channel ID */}
            <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4 mb-8">
                <h3 className="text-blue-400 font-medium mb-2">📘 How to get a Discord Channel ID</h3>
                <ol className="text-blue-300 text-sm space-y-1 list-decimal list-inside">
                    <li>Enable Developer Mode in Discord Settings → Advanced</li>
                    <li>Right-click on any channel</li>
                    <li>Click "Copy Channel ID"</li>
                    <li>Paste the ID in the field above</li>
                </ol>
            </div>

            {/* Channels List */}
            <div className="bg-gray-900 rounded-xl border border-gray-800 p-6">
                <h2 className="text-white text-xl font-semibold mb-4">Allowed Channels</h2>

                {loading ? (
                    <div className="text-gray-400">Loading...</div>
                ) : channels.length === 0 ? (
                    <div className="text-center py-8">
                        <div className="text-5xl mb-4">📭</div>
                        <p className="text-gray-400">No channels configured yet</p>
                        <p className="text-gray-500 text-sm mt-2">Add a channel above to get started</p>
                    </div>
                ) : (
                    <div className="space-y-3">
                        {channels.map((channel) => (
                            <div
                                key={channel.id}
                                className="flex items-center justify-between bg-gray-800 rounded-lg p-4 border border-gray-700"
                            >
                                <div>
                                    <p className="text-white font-medium">
                                        {channel.channel_name || 'Unnamed Channel'}
                                    </p>
                                    <p className="text-gray-400 text-sm font-mono">{channel.channel_id}</p>
                                    <p className="text-gray-500 text-xs mt-1">
                                        Added {new Date(channel.added_at).toLocaleDateString()}
                                    </p>
                                </div>

                                <button
                                    onClick={() => handleRemove(channel)}
                                    className="px-4 py-2 bg-red-600/20 text-red-400 border border-red-600/30 rounded-lg hover:bg-red-600/30 transition-all"
                                >
                                    Remove
                                </button>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    )
}
