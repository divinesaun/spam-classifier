
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from shared.database import supabase, create_user_api_key, list_user_api_keys, revoke_api_key
from shared.security import get_current_user

router = APIRouter()

class UserAuth(BaseModel):
    email: str
    password: str

class CreateKeyRequest(BaseModel):
    name: str = "Default Key"

class APIKeyResponse(BaseModel):
    key: str
    name: str
    created_at: str

@router.post("/signup")
async def signup(user: UserAuth):
    if not supabase:
        raise HTTPException(status_code=503, detail="Database unavailable")
    try:
        response = supabase.auth.sign_up({"email": user.email, "password": user.password})
        if response.user:
            return {"message": "User created successfully", "user": response.user}
        else:
             raise HTTPException(status_code=400, detail="Signup failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/signin")
async def signin(user: UserAuth):
    if not supabase:
        raise HTTPException(status_code=503, detail="Database unavailable")
    try:
        response = supabase.auth.sign_in_with_password({"email": user.email, "password": user.password})
        if response.session:
            return {"access_token": response.session.access_token, "token_type": "bearer"}
        else:
             raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- API Key Management ---

@router.post("/api-keys", response_model=APIKeyResponse)
async def create_key(request: CreateKeyRequest, user = Depends(get_current_user)):
    """Generates a new API key for the logged-in user."""
    result = await create_user_api_key(user.id, request.name)
    return APIKeyResponse(
        key=result.get("key"),
        name=result.get("name"),
        created_at=result.get("created_at")
    )

@router.get("/api-keys")
async def get_keys(user = Depends(get_current_user)):
    """Lists keys for the logged-in user."""
    return await list_user_api_keys(user.id)

@router.delete("/api-keys/{key}")
async def revoke_key(key: str, user = Depends(get_current_user)):
    """Revokes a specific key."""
    await revoke_api_key(user.id, key)
    return {"status": "revoked"}

# --- Analytics ---

@router.get("/analytics")
async def get_analytics(user = Depends(get_current_user)):
    """Retrieves usage analytics for the logged-in user."""
    from shared.database import get_user_usage_stats
    stats = await get_user_usage_stats(user.id)
    return stats
