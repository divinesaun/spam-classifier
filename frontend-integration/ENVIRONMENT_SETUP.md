# Environment Setup Guide

## Frontend Environment Variables

### Development (.env)
```env
# Backend API URL
VITE_BACKEND_URL=http://127.0.0.1:8000

# Optional: If you need Supabase client directly in frontend
# VITE_SUPABASE_URL=your_supabase_url
# VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

### Production (.env.production)
```env
# Production Backend URL
VITE_BACKEND_URL=https://spam-classifier-ba4i.vercel.app

# Optional: Supabase (if needed)
# VITE_SUPABASE_URL=your_supabase_url
# VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

---

## Backend Environment Variables

The backend requires these environment variables (already configured in your backend):

```env
# Supabase Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_service_role_key

# API Security (Optional)
SECRET_KEY=your_secret_key_for_jwt

# External APIs (for spam detection features)
VIRUSTOTAL_API_KEY=your_virustotal_api_key
GOOGLE_API_KEY=your_google_gemini_api_key

# Twilio (for WhatsApp webhook)
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
```

---

## Important Notes

### Frontend Token Storage
The API client stores the access token in `localStorage` with key: `access_token`

If you want to change this, update the key name in `api.ts`:
```typescript
// Change from 'access_token' to your preferred key name
localStorage.setItem('your_key_name', token);
```

### CORS Configuration
The backend is configured to accept requests from:
- `http://localhost:3000` (Create React App default)
- `http://localhost:5173` (Vite default)
- `http://localhost:4173` (Vite preview)

If your dev server runs on a different port, add it to the backend's `main.py`:
```python
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:4173",
    "http://localhost:YOUR_PORT",  # Add your port here
]
```

---

## Testing the Connection

### 1. Test Backend is Running
```bash
curl http://127.0.0.1:8000
# Should return: {"message": "Welcome to the Unified AI Backend..."}
```

### 2. Test API Documentation
Visit in browser: `http://127.0.0.1:8000/docs`

### 3. Test from Frontend (Browser Console)
```javascript
// Test basic connectivity
fetch('http://127.0.0.1:8000')
  .then(r => r.json())
  .then(console.log)

// Test signup (replace with your email/password)
fetch('http://127.0.0.1:8000/auth/signup', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'test@example.com',
    password: 'test123456'
  })
})
  .then(r => r.json())
  .then(console.log)
```

---

## Troubleshooting

### CORS Errors
**Symptom:** Browser console shows CORS policy error

**Solutions:**
1. Verify your frontend URL is in the backend's allowed origins
2. Ensure backend is running on the correct port
3. Check that CORS middleware is properly configured in `main.py`

### 401 Unauthorized
**Symptom:** "Invalid or expired token" error

**Solutions:**
1. Clear localStorage: `localStorage.clear()`
2. Sign in again to get a fresh token
3. Check that the token is being sent in the Authorization header

### Token Not Persisting
**Symptom:** User is logged out after page refresh

**Solutions:**
1. Verify token is being saved to localStorage after signin
2. Check that the token key name matches in save and retrieval
3. Ensure no code is clearing localStorage unintentionally

### Rate Limiting
**Symptom:** "Too many requests" error

**Solutions:**
1. Wait 60 seconds before retrying
2. Implement frontend rate limiting
3. Use different API keys for testing

---

## Security Checklist

- [ ] Never commit `.env` files to git (add to `.gitignore`)
- [ ] Use environment variables for all sensitive data
- [ ] Don't hardcode API keys in frontend code
- [ ] Enable HTTPS in production
- [ ] Implement proper error handling to avoid exposing sensitive info
- [ ] Regularly rotate API keys
- [ ] Monitor API usage for suspicious activity
- [ ] Use secure password requirements (min 6 chars, consider stronger)

---

## Next Steps

1. ✅ Configure your `.env` file
2. ✅ Start your backend: `uvicorn main:app --reload`
3. ✅ Start your frontend: `npm run dev`
4. ✅ Test the connection using browser dev tools
5. ✅ Implement authentication using example components
6. ✅ Build your UI around the provided API client

---

**Last Updated:** January 15, 2026
