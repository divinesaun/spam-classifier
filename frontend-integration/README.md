# Frontend Integration Guide

This directory contains the necessary files to integrate your React/Vite/Shadcn frontend with the Spam Classifier Backend.

## 1. API Client (`api.ts`)
The `api.ts` file uses Axios and includes an interceptor to automatically handle authentication for `/auth` routes.

### Usage:
1. Copy `api.ts` to your `src/lib/` or `src/utils/` folder.
2. Ensure you have `axios` installed (`npm install axios`).
3. Set `VITE_BACKEND_URL` in your `.env` file.

## 2. Authentication Flow
- Use `authApi.signup` and `authApi.signin` in your Auth forms.
- On successful sign-in, the backend returns an `access_token`. 
- Store this token (e.g., in `localStorage.setItem('supabase_token', token)`) so it can be picked up by the interceptor.

## 3. Managing API Keys
In your dashboard, use:
- `authApi.listApiKeys()` to fetch current keys.
- `authApi.createApiKey(name)` to generate a new `sc_...` key.
- `authApi.deleteApiKey(key)` to revoke a key.

## 4. Testing Spam Detection
The `/spam/detect_spam` endpoint requires an `X-API-Key` header.
```typescript
const response = await spamApi.detectSpam("Check this out: http://link.com", userApiKey);
```

## Backend Status:
- [x] Auth Routes (`/auth/signup`, `/auth/signin`)
- [x] API Key Management (`GET`, `POST`, `DELETE` on `/auth/api-keys`)
- [x] Prefix `sc_` added to all new keys for identification.
- [x] CORS configured to allow local development.
