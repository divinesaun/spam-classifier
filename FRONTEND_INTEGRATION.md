# Frontend Integration Guide

This guide explains how to connect your "AI Playground" frontend to the Spam Classifier backend to allow users to sign in and generate API keys.

## 1. Authentication (Frontend)

Your frontend should use **Supabase Auth** to handle user sign-in.

### Install Supabase Client
```bash
npm install @supabase/supabase-js
```

### Initialize Client
```javascript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient('YOUR_SUPABASE_URL', 'YOUR_SUPABASE_ANON_KEY')
```

### Sign In
```javascript
async function signIn() {
  const { data, error } = await supabase.auth.signInWithOAuth({
    provider: 'google',
  })
}
```

## 2. Managing API Keys

To generating keys, your frontend needs to talk to the Python Backend, passing the User's JWT (Access Token).

### Get the Session Token
```javascript
const { data: { session } } = await supabase.auth.getSession()
const token = session?.access_token
```

### Create a Key
Call the `POST /api-keys` endpoint on your Python backend.

```javascript
async function generateApiKey() {
  const { data: { session } } = await supabase.auth.getSession()
  
  const response = await fetch('http://localhost:8000/api-keys', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${session.access_token}` // Send JWT here
    },
    body: JSON.stringify({ name: "My App Key" })
  })
  
  const data = await response.json()
  console.log("New Key:", data.key)
}
```

### List Keys
```javascript
async function fetchKeys() {
  const { data: { session } } = await supabase.auth.getSession()
  
  const response = await fetch('http://localhost:8000/api-keys', {
    headers: {
      'Authorization': `Bearer ${session.access_token}`
    }
  })
  
  const keys = await response.json()
  return keys
}
```

## 3. Using the Service

Once users have their API Key (e.g., `abc123xym...`), they can use it in their own apps:

```bash
curl -X POST "http://localhost:8000/detect_spam" \
     -H "X-API-Key: abc123xym..." \
     -H "Content-Type: application/json" \
     -d '{"text": "Check this link http://suspicious.com"}'
```

## Database Setup

Ensure your `api_keys` table in Supabase has the following schema (created via `src/database.py` logic but good to verify):

```sql
create table api_keys (
  key text primary key,
  owner_id uuid references auth.users(id),
  name text,
  is_active boolean default true,
  created_at timestamptz default now()
);
```
