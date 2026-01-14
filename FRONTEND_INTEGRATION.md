"I have a unified Python (FastAPI) backend deployed at https://spam-classifier-ba4i.vercel.app/. I need to update my React + Vite + Shadcn frontend to connect to this new architecture.

The backend has three main routers:

auth/: Handles 
signup
, 
signin
, and api-keys management. (Requires Supabase JWT).
spam/
: Handles 
detect_spam
. (Requires an X-API-Key header).
moderator/: Content moderation placeholder.
Please implement the following in the frontend:

Shared Supabase Auth:
Ensure the frontend already uses @supabase/supabase-js.
On every request to /auth/*, include the session access token in the Authorization: Bearer <token> header.
API Client Setup:
Create an api.ts utility (using Axios or Fetch) with the base URL https://spam-classifier-ba4i.vercel.app/.
Include interceptors to automatically Attach the Supabase JWT for auth routes.
Authentication UI:
Update the Sign In/Sign Up flow to point to the backend's /auth/signin and /auth/signup endpoints to sync users.
Create an API Keys Dashboard section using Shadcn components (Table, Button, Dialog) to:
GET /auth/api-keys: List existing keys.
POST /auth/api-keys: Create a new key (provide a name).
DELETE /auth/api-keys/{key}: Revoke a key.
Spam Classifier Integration:
In the Spam Checker component, send the user's message to POST /spam/detect_spam.
Crucial: This route expects the header X-API-Key. For the user's "own" requests from the dashboard, use their generated API key from the database.
Environment Variables:
Set VITE_BACKEND_URL=https://spam-classifier-ba4i.vercel.app/.
Response Format: Provide the code for the api.ts client, the API Key Management component, and the updated Spam Detection service call."

Quick Reference for you:
Base URL: https://spam-classifier-ba4i.vercel.app/
Auth Prefix: /auth (Use Bearer JWT)
Spam Prefix: /spam (Use X-API-Key header)
Moderator Prefix: /moderator