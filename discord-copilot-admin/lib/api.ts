const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface ApiError {
    detail: string
}

export async function apiRequest<T>(
    endpoint: string,
    options?: RequestInit
): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`

    const response = await fetch(url, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...options?.headers,
        },
    })

    if (!response.ok) {
        const error: ApiError = await response.json()
        throw new Error(error.detail || 'API request failed')
    }

    return response.json()
}

export async function apiRequestWithAuth<T>(
    endpoint: string,
    token: string,
    options?: RequestInit
): Promise<T> {
    return apiRequest<T>(endpoint, {
        ...options,
        headers: {
            ...options?.headers,
            Authorization: `Bearer ${token}`,
        },
    })
}
