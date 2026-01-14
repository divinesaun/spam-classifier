from fastapi import Security, HTTPException, status, Depends
from fastapi.security import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials
from shared.database import get_api_key, supabase
import os
import logging

logger = logging.getLogger(__name__)

# --- API Key Security (For External Apps) ---
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
MASTER_API_KEY = os.environ.get("MASTER_API_KEY")

async def verify_api_key(api_key: str = Security(api_key_header)):
    """
    Verifies the API Key provided in the header.
    Used by external applications consuming the Spam Detection API.
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    # Check Master Key
    if MASTER_API_KEY and api_key == MASTER_API_KEY:
        return api_key

    # Check Database
    key_record = await get_api_key(api_key)
    if key_record:
        return key_record

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid API Key",
    )

# --- JWT Security (For Frontend Dashboard) ---
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Validates the Supabase JWT sent by the frontend functionality.
    Returns the user object if valid.
    """
    token = credentials.credentials
    
    if not supabase:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Database connection not available"
        )
        
    try:
        # Verify the token with Supabase Auth
        user_response = supabase.auth.get_user(token)
        if not user_response or not user_response.user:
             raise HTTPException(status_code=401, detail="Invalid Authentication Token")
        
        return user_response.user
        
    except Exception as e:
        logger.error(f"JWT Validation Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
