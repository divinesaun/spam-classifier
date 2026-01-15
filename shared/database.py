import os
import logging
import secrets
import string
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)
load_dotenv()

# Initialize Supabase Client
url: str = os.environ.get("SUPABASE_URL", "")
key: str = os.environ.get("SUPABASE_KEY", "")

supabase: Optional[Client] = None

if url and key:
    try:
        supabase = create_client(url, key)
        logger.info("Supabase client initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")
else:
    logger.warning("SUPABASE_URL or SUPABASE_KEY not set. Database features will be disabled.")



API_KEYS_TABLE = "api_keys"

# --- API Key Management Functions ---

async def get_api_key(key_value: str):
    """Retrieves an API key record if valid."""
    if not supabase: return None
    try:
        response = supabase.table(API_KEYS_TABLE).select("*").eq("key", key_value).eq("is_active", True).execute()
        if response.data:
            return response.data[0]
    except Exception as e:
        logger.error(f"Error validating API key: {e}")
    return None

async def create_user_api_key(user_id: str, name: str = "Default Key") -> Dict[str, Any]:
    """Generates and saves a new API key for a user."""
    if not supabase: raise Exception("Database unavailable")
    
    # Generate Key
    alphabet = string.ascii_letters + string.digits
    new_key = f"sc_{''.join(secrets.choice(alphabet) for i in range(32))}"
    
    data = {
        "key": new_key,
        "owner_id": user_id,
        "name": name,
        "is_active": True
    }
    
    try:
        response = supabase.table(API_KEYS_TABLE).insert(data).execute()
        if response.data:
            return response.data[0]
    except Exception as e:
        logger.error(f"Error creating API key: {e}")
        raise e
    return {}

async def list_user_api_keys(user_id: str) -> List[Dict[str, Any]]:
    """Lists all active API keys for a user."""
    if not supabase: return []
    try:
        response = supabase.table(API_KEYS_TABLE).select("*").eq("owner_id", user_id).order("created_at", desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        logger.error(f"Error listing API keys: {e}")
        return []

async def revoke_api_key(user_id: str, key_to_revoke: str):
    """Revokes (deletes or deactivates) an API Key."""
    if not supabase: return
    try:
        # We enforce owner_id match for security
        supabase.table(API_KEYS_TABLE).delete().eq("key", key_to_revoke).eq("owner_id", user_id).execute()
    except Exception as e:
        logger.error(f"Error revoking API key: {e}")
        raise e
