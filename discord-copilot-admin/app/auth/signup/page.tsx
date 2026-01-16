'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { supabase } from '@/lib/supabase'
import Link from 'next/link'

export default function SignupPage() {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const [success, setSuccess] = useState(false)
    const router = useRouter()

    const handleSignup = async (e: React.FormEvent) => {
        e.preventDefault()
        setError('')
        setLoading(true)

        if (password !== confirmPassword) {
            setError('Passwords do not match')
            setLoading(false)
            return
        }

        if (password.length < 6) {
            setError('Password must be at least 6 characters')
            setLoading(false)
            return
        }

        try {
            const { data, error } = await supabase.auth.signUp({
                email,
                password,
            })

            if (error) throw error

            setSuccess(true)
            setTimeout(() => {
                router.push('/auth/login')
            }, 2000)
        } catch (error: any) {
            setError(error.message)
        } finally {
            setLoading(false)
        }
    }

    if (success) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500">
                <div className="bg-white/10 backdrop-blur-lg p-8 rounded-2xl shadow-2xl w-full max-w-md border border-white/20 text-center">
                    <div className="text-6xl mb-4">✅</div>
                    <h2 className="text-2xl font-bold text-white mb-2">Account Created!</h2>
                    <p className="text-white/80">Redirecting to login...</p>
                </div>
            </div>
        )
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500">
            <div className="bg-white/10 backdrop-blur-lg p-8 rounded-2xl shadow-2xl w-full max-w-md border border-white/20">
                <div className="text-center mb-8">
                    <h1 className="text-4xl font-bold text-white mb-2">Create Account</h1>
                    <p className="text-white/80">Join Discord Copilot</p>
                </div>

                <form onSubmit={handleSignup} className="space-y-6">
                    {error && (
                        <div className="bg-red-500/20 border border-red-500/50 text-white px-4 py-3 rounded-lg">
                            {error}
                        </div>
                    )}

                    <div>
                        <label htmlFor="email" className="block text-white text-sm font-medium mb-2">
                            Email
                        </label>
                        <input
                            id="email"
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            className="w-full px-4 py-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/50"
                            placeholder="you@example.com"
                        />
                    </div>

                    <div>
                        <label htmlFor="password" className="block text-white text-sm font-medium mb-2">
                            Password
                        </label>
                        <input
                            id="password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            className="w-full px-4 py-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/50"
                            placeholder="••••••••"
                        />
                    </div>

                    <div>
                        <label htmlFor="confirmPassword" className="block text-white text-sm font-medium mb-2">
                            Confirm Password
                        </label>
                        <input
                            id="confirmPassword"
                            type="password"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            required
                            className="w-full px-4 py-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/50"
                            placeholder="••••••••"
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full py-3 px-4 bg-white text-purple-600 rounded-lg font-semibold hover:bg-white/90 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                    >
                        {loading ? 'Creating account...' : 'Sign Up'}
                    </button>
                </form>

                <p className="mt-6 text-center text-white/80 text-sm">
                    Already have an account?{' '}
                    <Link href="/auth/login" className="text-white font-semibold hover:underline">
                        Sign in
                    </Link>
                </p>
            </div>
        </div>
    )
}
