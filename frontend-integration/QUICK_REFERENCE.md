# Frontend Integration - Quick Reference Card

## 🎯 What You Have

Your spam classifier backend is **fully functional** and provides these endpoints:

| Endpoint | Method | Auth Required | Purpose |
|----------|--------|---------------|---------|
| `/auth/signup` | POST | No | Create new user account |
| `/auth/signin` | POST | No | Login and get access token |
| `/auth/api-keys` | GET | Bearer Token | List user's API keys |
| `/auth/api-keys` | POST | Bearer Token | Create new API key |
| `/auth/api-keys/{key}` | DELETE | Bearer Token | Revoke API key |
| `/spam/detect_spam` | POST | X-API-Key | Analyze text for spam |

---

## 📂 Files in This Directory

| File | Purpose | When to Use |
|------|---------|-------------|
| `COMPREHENSIVE_INTEGRATION_GUIDE.md` | **START HERE** - Complete reference | Read first for full details |
| `api.ts` | Ready-to-use TypeScript API client | Copy to your project |
| `example-components.tsx` | Ready-to-use React components | Copy & customize for your UI |
| `ENVIRONMENT_SETUP.md` | Environment configuration guide | When setting up .env files |
| `README.md` | Quick overview | Quick reference |
| `QUICK_REFERENCE.md` | This file | At-a-glance summary |

---

## ⚡ 5-Minute Integration

### 1. Copy Files
```bash
cp api.ts /path/to/your/frontend/src/lib/
```

### 2. Install Dependencies
```bash
npm install axios
```

### 3. Configure Environment
Create `.env`:
```env
VITE_BACKEND_URL=http://127.0.0.1:8000
```

### 4. Use in Your Components
```typescript
import { authApi, spamApi } from '@/lib/api';

// Sign in
const { data } = await authApi.signin({ email, password });
localStorage.setItem('access_token', data.access_token);

// Create API key
const keyData = await authApi.createApiKey({ name: 'My Key' });

// Detect spam
const result = await spamApi.detectSpam(text, apiKey);
```

---

## 🔐 Authentication Flow

```
┌─────────────┐
│ 1. Sign Up  │  POST /auth/signup
│   or        │  { email, password }
│ 2. Sign In  │  POST /auth/signin → Get access_token
└──────┬──────┘
       │
       v
┌────────────────────────┐
│ Store Token            │  localStorage.setItem('access_token', token)
└──────┬─────────────────┘
       │
       v
┌────────────────────────┐
│ Create API Key         │  POST /auth/api-keys (Bearer: token)
│                        │  → Get API key (sc_...)
└──────┬─────────────────┘
       │
       v
┌────────────────────────┐
│ Use API Key            │  POST /spam/detect_spam (X-API-Key: sc_...)
│                        │  → Get spam analysis
└────────────────────────┘
```

---

## 📝 Request/Response Examples

### Sign Up
```typescript
// Request
POST /auth/signup
{
  "email": "user@example.com",
  "password": "securepass123"
}

// Response (200)
{
  "message": "User created successfully",
  "user": {
    "id": "7e3082ec-22bc-4be1-9a3d-04d0af4a1030",
    "email": "user@example.com"
  }
}
```

### Sign In
```typescript
// Request
POST /auth/signin
{
  "email": "user@example.com",
  "password": "securepass123"
}

// Response (200)
{
  "access_token": "eyJhbGciOiJFUzI1NiIs...",
  "token_type": "bearer"
}
```

### Create API Key
```typescript
// Request
POST /auth/api-keys
Headers: { Authorization: "Bearer <token>" }
{
  "name": "Production Key"
}

// Response (200)
{
  "key": "sc_1a2b3c4d5e6f7g8h9i0j",
  "name": "Production Key",
  "created_at": "2026-01-15T12:00:00Z"
}
```

### Detect Spam
```typescript
// Request
POST /spam/detect_spam
Headers: { X-API-Key: "sc_your_key_here" }
{
  "text": "Click here to win: http://suspicious.com"
}

// Response (200)
{
  "is_spam": true,
  "confidence": 85,
  "response_text": "⚠️ SPAM DETECTED...",
  "details": { ... }
}
```

---

## 🛠️ Common Tasks

### Check if User is Logged In
```typescript
const isLoggedIn = !!localStorage.getItem('access_token');
```

### Logout User
```typescript
localStorage.removeItem('access_token');
window.location.href = '/login';
```

### Handle API Errors
```typescript
import { handleApiError } from '@/lib/api';

try {
  await authApi.signin({ email, password });
} catch (error) {
  const message = handleApiError(error);
  alert(message);
}
```

### Copy API Key to Clipboard
```typescript
await navigator.clipboard.writeText(apiKey);
alert('API key copied!');
```

---

## ⚠️ Important Limits

| Limit | Value | Notes |
|-------|-------|-------|
| Min Password Length | 6 characters | Supabase default |
| Rate Limit (Spam Detection) | 5 requests/min | Per API key |
| API Key Prefix | `sc_` | All keys start with this |
| Token Storage | `localStorage` | Key: `access_token` |

---

## 🐛 Quick Troubleshooting

| Error | Solution |
|-------|----------|
| CORS error | Add your URL to backend's allowed origins |
| 401 Unauthorized | Clear localStorage and login again |
| 429 Too Many Requests | Wait 60 seconds before retrying |
| API key doesn't work | Ensure you're sending it in `X-API-Key` header |

---

## 📚 Where to Find What

- **Complete API schemas** → `COMPREHENSIVE_INTEGRATION_GUIDE.md`
- **Environment setup** → `ENVIRONMENT_SETUP.md`
- **Ready-to-use components** → `example-components.tsx`
- **TypeScript client** → `api.ts`
- **This cheat sheet** → `QUICK_REFERENCE.md`

---

## ✅ Pre-flight Checklist

Before you start integrating:

1. [ ] Backend is running (`http://127.0.0.1:8000`)
2. [ ] You can access `/docs` in your browser
3. [ ] You've tested signup/signin in `/docs`
4. [ ] Frontend dev server runs on allowed CORS origin
5. [ ] `.env` file is configured with `VITE_BACKEND_URL`
6. [ ] `axios` is installed in your frontend
7. [ ] You've read the comprehensive guide

---

## 🚀 Ready to Build!

1. Copy `api.ts` to your project
2. Copy components from `example-components.tsx`
3. Customize the UI to match your design
4. Test thoroughly using the backend `/docs`
5. Deploy and enjoy! 🎉

---

**Need Help?** Check `COMPREHENSIVE_INTEGRATION_GUIDE.md` for detailed explanations.

**Last Updated:** January 15, 2026
