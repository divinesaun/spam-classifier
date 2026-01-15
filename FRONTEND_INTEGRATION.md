# Frontend Integration Guide & Prompt

This document provides a comprehensive guide and a ready-to-use prompt for integrating the **Spam Classifier Backend** with a static frontend (React, Vite, Shadcn).

## Backend Overview
- **Base URL**: `https://spam-classifier-ba4i.vercel.app/`
- **Authentication**: 
  - **User Auth**: Bearer JWT (Supabase) for `/auth` routes.
  - **API Usage**: `X-API-Key` header for `/spam` routes.

---

## 1. Endpoint Schemas

### Authentication (`/auth`)
All auth routes (except signup/signin) require `Authorization: Bearer <JWT_TOKEN>`.

#### `POST /auth/signup`
Creates a new user in Supabase and syncs with the backend.
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "message": "User created successfully",
    "user": { "id": "uuid", "email": "..." }
  }
  ```

#### `POST /auth/signin`
Authenticates a user and returns a JWT.
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "access_token": "eyJhbG...",
    "token_type": "bearer"
  }
  ```

#### `GET /auth/api-keys`
Lists all API keys for the authenticated user.
- **Response (200 OK)**:
  ```json
  [
    {
      "key": "sc_...",
      "name": "My Website Key",
      "created_at": "2024-03-20T10:00:00Z"
    }
  ]
  ```

#### `POST /auth/api-keys`
Generates a new API key.
- **Request Body**:
  ```json
  {
    "name": "Production Key"
  }
  ```
- **Response (201 Created)**:
  ```json
  {
    "key": "sc_live_abc123...",
    "name": "Production Key",
    "created_at": "2024-03-20T10:00:00Z"
  }
  ```

---

### Spam Detection (`/spam`)
Requires `X-API-Key` header.

#### `POST /spam/detect_spam`
Analyzes a message for spam/scams.
- **Request Body**:
  ```json
  {
    "text": "Check out this link: http://malicious-site.com"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "url": "http://malicious-site.com",
    "domain": "malicious-site.com",
    "verdict": "SCAM",
    "risk_score": 90,
    "response_text": "Detailed LLM analysis here...",
    "full_report": {
      "whois": { ... },
      "virus_total": { ... }
    }
  }
  ```

---

## 2. The Integration Prompt
*Copy and paste the text below into your frontend development chat (e.g., with an AI or a developer).*

---

### 🚀 PROMPT: Connect Static Frontend to Spam Classifier Backend

I need to connect this static React/Vite frontend to a Python FastAPI backend hosted at `https://spam-classifier-ba4i.vercel.app/`. The frontend is currently just UI shells and needs full logic implementation.

**Core Requirements:**

1.  **API Client Setup**:
    *   Create an `api.ts` utility using Axios.
    *   Base URL: `https://spam-classifier-ba4i.vercel.app/`
    *   Add an interceptor to automatically attach the Supabase access token as a `Bearer` token in the `Authorization` header for any requests to the `/auth/` endpoints.

2.  **Authentication Flow**:
    *   Update the `LoginForm` and `SignupForm` to use the backend endpoints:
        *   `POST /auth/signup`
        *   `POST /auth/signin`
    *   Store the returned `access_token` in the Supabase auth state or local storage so the interceptor can use it.

3.  **API Key Management (Dashboard)**:
    *   Build/Update the Dashboard to manage API keys.
    *   Use `GET /auth/api-keys` to list keys.
    *   Use `POST /auth/api-keys` (schema: `{ "name": string }`) to create keys.
    *   Use `DELETE /auth/api-keys/{key}` to revoke keys.

4.  **Spam Checker Implementation**:
    *   When a user clicks "Check for Spam", send a `POST` request to `/spam/detect_spam` with the body `{ "text": string }`.
    *   **CRITICAL**: This endpoint requires the `X-API-Key` header. 
    *   *Implementation Logic*: Since this is the dashboard, the frontend should fetch the user's active API keys from the backend and use the first available `sc_...` key in the header.

5.  **Environment Variables**:
    *   Use `VITE_BACKEND_URL` for the base URL.

**Backend Schema Reference:**
- **Analyze Response**: `{ url, domain, verdict, risk_score, response_text, full_report }`
- **API Key Item**: `{ key, name, created_at }`

Please provide the updated `api.ts`, the Auth logic, and the Dashboard components (using Shadcn/UI where possible).

---