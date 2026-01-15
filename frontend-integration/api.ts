import axios, { AxiosError } from 'axios';

// Backend URL from environment variables
const API_URL = import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:8000';

// Create axios instance
export const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add auth token
api.interceptors.request.use(
    async (config) => {
        // Add Bearer token to protected /auth routes (except signup/signin)
        const isAuthRoute = config.url?.startsWith('/auth/');
        const isPublicAuth = config.url === '/auth/signup' || config.url === '/auth/signin';

        if (isAuthRoute && !isPublicAuth) {
            const token = localStorage.getItem('access_token');
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
        }

        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor for error handling
api.interceptors.response.use(
    (response) => response,
    (error: AxiosError<{ detail: string }>) => {
        // Handle specific error cases
        if (error.response?.status === 401) {
            // Token expired or invalid - redirect to login
            localStorage.removeItem('access_token');
            // Uncomment below if you want auto-redirect to login
            // window.location.href = '/login';
        }

        return Promise.reject(error);
    }
);

// TypeScript interfaces
export interface SignupRequest {
    email: string;
    password: string;
}

export interface SigninRequest {
    email: string;
    password: string;
}

export interface SignupResponse {
    message: string;
    user: {
        id: string;
        email: string;
    };
}

export interface SigninResponse {
    access_token: string;
    token_type: string;
}

export interface ApiKey {
    key: string;
    name: string;
    created_at: string;
}

export interface CreateApiKeyRequest {
    name?: string;
}

export interface DetectSpamRequest {
    text: string;
}

export interface AnalysisResult {
    response_text: string;
    is_spam: boolean;
    confidence: number;
    details: Record<string, any>;
}

// Auth API methods
export const authApi = {
    signup: (data: SignupRequest) =>
        api.post<SignupResponse>('/auth/signup', data),

    signin: (data: SigninRequest) =>
        api.post<SigninResponse>('/auth/signin', data),

    listApiKeys: () =>
        api.get<ApiKey[]>('/auth/api-keys'),

    createApiKey: (data: CreateApiKeyRequest) =>
        api.post<ApiKey>('/auth/api-keys', data),

    deleteApiKey: (key: string) =>
        api.delete<{ status: string }>(`/auth/api-keys/${key}`),
};

// Spam detection API methods
export const spamApi = {
    detectSpam: (text: string, apiKey: string) =>
        api.post<AnalysisResult>(
            '/spam/detect_spam',
            { text },
            {
                headers: {
                    'X-API-Key': apiKey,
                },
            }
        ),
};

// Error handling helper
export function handleApiError(error: unknown): string {
    if (error instanceof AxiosError) {
        const status = error.response?.status;
        const detail = error.response?.data?.detail;

        switch (status) {
            case 400:
                return `Bad Request: ${detail || 'Invalid input'}`;

            case 401:
                return 'Session expired. Please login again.';

            case 403:
                return 'Access forbidden. Check your API key.';

            case 404:
                return 'Resource not found';

            case 429:
                return 'Rate limit exceeded. Please wait before trying again.';

            case 503:
                return 'Service temporarily unavailable. Please try again later.';

            default:
                return detail || 'An unexpected error occurred';
        }
    }

    return 'Network error. Please check your connection.';
}
