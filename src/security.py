from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from src.database import get_api_key
import os
import logging

logger = logging.getLogger(__name__)

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Allow a master key from environment for development/fallback
MASTER_API_KEY = os.environ.get("MASTER_API_KEY")

async def verify_api_key(api_key: str = Security(api_key_header)):
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

    # If we fall through, invalid
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid API Key",
    )
