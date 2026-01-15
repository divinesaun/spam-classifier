import axios from 'axios';

// The Backend URL from environment variables
const API_URL = import.meta.env.VITE_BACKEND_URL || 'https://spam-classifier-ba4i.vercel.app';

export const api = axios.create({
    baseURL: API_URL,
});

// Interceptor to add Supabase JWT token to /auth requests
api.interceptors.request.use(async (config) => {
    // Check if it's an /auth request (except signup/signin which don't need the token yet)
    const isAuthRoute = config.url?.startsWith('/auth/');
    const isPublicAuth = config.url === '/auth/signup' || config.url === '/auth/signin';

    if (isAuthRoute && !isPublicAuth) {
        // Replace this with your actual method of getting the Supabase session token
        // e.g., const { data } = await supabase.auth.getSession();
        const token = localStorage.getItem('supabase_token');

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
    }

    return config;
}, (error) => {
    return Promise.reject(error);
});

export const authApi = {
    signup: (email, password) => api.post('/auth/signup', { email, password }),
    signin: (email, password) => api.post('/auth/signin', { email, password }),
    listApiKeys: () => api.get('/auth/api-keys'),
    createApiKey: (name) => api.post('/auth/api-keys', { name }),
    deleteApiKey: (key) => api.delete(`/auth/api-keys/${key}`),
};

export const spamApi = {
    detectSpam: (text, apiKey) => api.post('/spam/detect_spam', { text }, {
        headers: {
            'X-API-Key': apiKey
        }
    }),
};
