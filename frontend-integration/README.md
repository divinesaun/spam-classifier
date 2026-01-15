# Frontend Integration Files

This directory contains everything you need to integrate your React/Vite frontend with the Spam Classifier Backend API.

## 📚 Quick Links

- **[COMPREHENSIVE_INTEGRATION_GUIDE.md](./COMPREHENSIVE_INTEGRATION_GUIDE.md)** - *Start here!* Complete guide with detailed schemas, examples, and best practices
- **[api.ts](./api.ts)** - Ready-to-use TypeScript API client

---

## 🚀 Quick Start

### 1. Read the Comprehensive Guide
Open `COMPREHENSIVE_INTEGRATION_GUIDE.md` for:
- Complete API endpoint documentation with request/response schemas
- Step-by-step implementation guide
- Authentication flow diagrams
- Error handling strategies
- Security best practices
- Troubleshooting tips

### 2. Copy the API Client
```bash
# Copy api.ts to your project
cp api.ts /path/to/your/frontend/src/lib/
```

### 3. Install Dependencies
```bash
npm install axios
```

### 4. Configure Environment
Create `.env` in your frontend root:
```env
VITE_BACKEND_URL=http://127.0.0.1:8000
```

### 5. Implement Authentication
Follow the examples in the comprehensive guide to:
- Create login/signup forms
- Set up AuthContext
- Manage API keys
- Implement spam detection

---

## 📁 What's Included

### `COMPREHENSIVE_INTEGRATION_GUIDE.md`
A complete reference document containing:
- ✅ All API endpoints with exact schemas
- ✅ TypeScript interfaces for type safety
- ✅ Complete React component examples
- ✅ Authentication flow explanation
- ✅ Token management strategies
- ✅ Error handling patterns
- ✅ Security best practices
- ✅ Testing checklist

### `api.ts`
A production-ready Axios client with:
- ✅ Automatic token injection for authenticated routes
- ✅ Request/response interceptors
- ✅ TypeScript interfaces
- ✅ Error handling utilities
- ✅ All API methods (auth, API keys, spam detection)

---

## 🔐 Authentication Flow Summary

```
1. User signs up     → POST /auth/signup
2. User signs in     → POST /auth/signin → Receive access_token
3. Store token       → localStorage.setItem('access_token', token)
4. Create API key    → POST /auth/api-keys (with Bearer token)
5. Use API key       → POST /spam/detect_spam (with X-API-Key header)
```

---

## 📡 Backend Endpoints

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/signin` - Login and get access token

### API Key Management (Requires Bearer Token)
- `GET /auth/api-keys` - List user's API keys
- `POST /auth/api-keys` - Create new API key
- `DELETE /auth/api-keys/{key}` - Revoke API key

### Spam Detection (Requires X-API-Key)
- `POST /spam/detect_spam` - Analyze text for spam

---

## 🎯 Usage Examples

### Sign In
```typescript
import { authApi } from '@/lib/api';

const { data } = await authApi.signin({
  email: 'user@example.com',
  password: 'password123'
});

localStorage.setItem('access_token', data.access_token);
```

### Create API Key
```typescript
import { authApi } from '@/lib/api';

const { data } = await authApi.createApiKey({
  name: 'My App Key'
});

console.log('New key:', data.key); // sc_...
```

### Detect Spam
```typescript
import { spamApi } from '@/lib/api';

const { data } = await spamApi.detectSpam(
  'Check this link: http://example.com',
  'sc_your_api_key_here'
);

console.log('Is spam:', data.is_spam);
console.log('Confidence:', data.confidence);
```

---

## ⚠️ Important Notes

### Token Storage
- Access tokens are stored in `localStorage` as `access_token`
- Tokens are automatically added to requests via interceptor
- Change the key name in `api.ts` if needed

### API Keys
- All new keys have `sc_` prefix
- Keys are required for spam detection endpoint
- Users must be authenticated to create/manage keys

### Rate Limiting
- Spam detection: **5 requests/minute** per API key
- Handle 429 errors gracefully in your UI

### CORS
Backend allows these origins:
- `http://localhost:3000`
- `http://localhost:5173`
- `http://localhost:4173`

---

## 🐛 Troubleshooting

### "CORS Error"
→ Ensure your dev server runs on an allowed origin

### "Invalid or expired token"
→ Clear `localStorage` and login again

### "Rate limit exceeded"
→ Wait 60 seconds before retrying

**For detailed troubleshooting, see the comprehensive guide.**

---

## 📞 Next Steps

1. **Read** `COMPREHENSIVE_INTEGRATION_GUIDE.md`
2. **Copy** `api.ts` to your project
3. **Configure** environment variables
4. **Implement** the examples from the guide
5. **Test** the integration using `/docs` on the backend

---

**Last Updated:** January 15, 2026
