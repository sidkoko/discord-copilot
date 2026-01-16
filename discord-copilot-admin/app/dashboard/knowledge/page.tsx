'use client'

import { useState, useEffect, useRef } from 'react'
import { supabase } from '@/lib/supabase'
import { apiRequestWithAuth } from '@/lib/api'

interface Document {
    id: string
    filename: string
    file_size: number
    upload_date: string
    status: string
}

export default function KnowledgePage() {
    const [documents, setDocuments] = useState<Document[]>([])
    const [loading, setLoading] = useState(true)
    const [uploading, setUploading] = useState(false)
    const [error, setError] = useState('')
    const [success, setSuccess] = useState('')
    const fileInputRef = useRef<HTMLInputElement>(null)

    useEffect(() => {
        fetchDocuments()
    }, [])

    const fetchDocuments = async () => {
        try {
            const { data: { session } } = await supabase.auth.getSession()
            if (!session) return

            const data = await apiRequestWithAuth<Document[]>(
                '/api/knowledge/list',
                session.access_token
            )
            setDocuments(data)
        } catch (error: any) {
            setError('Failed to fetch documents')
        } finally {
            setLoading(false)
        }
    }

    const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0]
        if (!file) return

        // Validate file type
        if (!file.name.endsWith('.pdf')) {
            setError('Only PDF files are allowed')
            return
        }

        // Validate file size (10MB)
        if (file.size > 10 * 1024 * 1024) {
            setError('File size must be less than 10MB')
            return
        }

        setUploading(true)
        setError('')
        setSuccess('')

        try {
            const { data: { session } } = await supabase.auth.getSession()
            if (!session) throw new Error('Not authenticated')

            const formData = new FormData()
            formData.append('file', file)

            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/knowledge/upload`, {
                method: 'POST',
                headers: {
                    Authorization: `Bearer ${session.access_token}`,
                },
                body: formData,
            })

            if (!response.ok) {
                const errorData = await response.json()
                throw new Error(errorData.detail || 'Upload failed')
            }

            setSuccess(`✅ ${file.name} uploaded successfully! Processing...`)
            fetchDocuments()

            // Clear file input
            if (fileInputRef.current) {
                fileInputRef.current.value = ''
            }
        } catch (error: any) {
            setError(error.message)
        } finally {
            setUploading(false)
        }
    }

    const handleDelete = async (documentId: string, filename: string) => {
        if (!confirm(`Are you sure you want to delete "${filename}"?`)) return

        try {
            const { data: { session } } = await supabase.auth.getSession()
            if (!session) return

            await apiRequestWithAuth(
                `/api/knowledge/${documentId}`,
                session.access_token,
                { method: 'DELETE' }
            )

            setSuccess(`✅ ${filename} deleted successfully`)
            fetchDocuments()
        } catch (error: any) {
            setError(`Failed to delete ${filename}`)
        }
    }

    const formatFileSize = (bytes: number) => {
        if (bytes < 1024) return bytes + ' B'
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB'
        return (bytes / (1024 * 1024)).toFixed(2) + ' MB'
    }

    const getStatusBadge = (status: string) => {
        const badges = {
            processing: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
            completed: 'bg-green-500/20 text-green-400 border-green-500/30',
            failed: 'bg-red-500/20 text-red-400 border-red-500/30',
        }
        return badges[status as keyof typeof badges] || badges.processing
    }

    return (
        <div className="max-w-6xl">
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-white mb-2">Knowledge Base</h1>
                <p className="text-gray-400">Upload PDFs to power your bot with domain knowledge</p>
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

            {/* Upload Section */}
            <div className="bg-gray-900 rounded-xl border border-gray-800 p-6 mb-8">
                <h2 className="text-white text-xl font-semibold mb-4">Upload PDF</h2>

                <div className="border-2 border-dashed border-gray-700 rounded-lg p-8 text-center hover:border-purple-500 transition-all">
                    <input
                        ref={fileInputRef}
                        type="file"
                        accept=".pdf"
                        onChange={handleUpload}
                        disabled={uploading}
                        className="hidden"
                        id="fileInput"
                    />
                    <label
                        htmlFor="fileInput"
                        className="cursor-pointer"
                    >
                        <div className="text-5xl mb-4">📄</div>
                        <p className="text-white font-medium mb-2">
                            {uploading ? 'Uploading...' : 'Click to upload PDF'}
                        </p>
                        <p className="text-gray-400 text-sm">Maximum file size: 10MB</p>
                    </label>
                </div>
            </div>

            {/* Documents List */}
            <div className="bg-gray-900 rounded-xl border border-gray-800 p-6">
                <h2 className="text-white text-xl font-semibold mb-4">Uploaded Documents</h2>

                {loading ? (
                    <div className="text-gray-400">Loading...</div>
                ) : documents.length === 0 ? (
                    <div className="text-center py-8">
                        <div className="text-5xl mb-4">📭</div>
                        <p className="text-gray-400">No documents uploaded yet</p>
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead>
                                <tr className="border-b border-gray-800">
                                    <th className="text-left text-gray-400 font-medium py-3 px-4">Filename</th>
                                    <th className="text-left text-gray-400 font-medium py-3 px-4">Size</th>
                                    <th className="text-left text-gray-400 font-medium py-3 px-4">Uploaded</th>
                                    <th className="text-left text-gray-400 font-medium py-3 px-4">Status</th>
                                    <th className="text-left text-gray-400 font-medium py-3 px-4">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {documents.map((doc) => (
                                    <tr key={doc.id} className="border-b border-gray-800 hover:bg-gray-800/50">
                                        <td className="py-3 px-4 text-white">{doc.filename}</td>
                                        <td className="py-3 px-4 text-gray-400">{formatFileSize(doc.file_size)}</td>
                                        <td className="py-3 px-4 text-gray-400">
                                            {new Date(doc.upload_date).toLocaleDateString()}
                                        </td>
                                        <td className="py-3 px-4">
                                            <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getStatusBadge(doc.status)}`}>
                                                {doc.status}
                                            </span>
                                        </td>
                                        <td className="py-3 px-4">
                                            <button
                                                onClick={() => handleDelete(doc.id, doc.filename)}
                                                className="text-red-400 hover:text-red-300 transition-colors"
                                            >
                                                🗑️ Delete
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    )
}
