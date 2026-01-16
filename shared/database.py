import os
import logging
import secrets
import string
from datetime import datetime, timedelta
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
API_USAGE_TABLE = "api_usage"


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
    new_key = ''.join(secrets.choice(alphabet) for i in range(32))
    
    data = {
        "key": new_key,
        "owner_id": user_id,  # Linked to the Supabase User ID
        "name": name,
        "is_active": True,
        "created_at": datetime.now().isoformat()
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

# --- API Usage & Analytics ---

async def log_api_usage(api_key: str, endpoint: str, method: str, status_code: int):
    """Logs an API request for analytics."""
    if not supabase: return
    data = {
        "api_key": api_key,
        "endpoint": endpoint,
        "method": method,
        "status_code": status_code,
        "timestamp": datetime.now().isoformat()
    }
    try:
        supabase.table(API_USAGE_TABLE).insert(data).execute()
    except Exception as e:
        logger.error(f"Error logging API usage: {e}")

async def get_user_usage_stats(user_id: str) -> Dict[str, Any]:
    """Retrieves aggregated usage statistics for a user's API keys."""
    if not supabase: return {}
    
    try:
        # 1. Get all API keys for this user
        keys_response = supabase.table(API_KEYS_TABLE).select("key").eq("owner_id", user_id).execute()
        key_strings = [k["key"] for k in keys_response.data] if keys_response.data else []
        
        if not key_strings:
            return {
                "total_requests": 0,
                "recent_requests_24h": 0,
                "daily_stats": []
            }

        # 2. Get total requests
        total_resp = supabase.table(API_USAGE_TABLE).select("id", count="exact").in_("api_key", key_strings).execute()
        total_requests = total_resp.count if total_resp.count is not None else 0

        # 3. Get requests in last 24h
        yesterday = (datetime.now() - timedelta(days=1)).isoformat()
        recent_resp = supabase.table(API_USAGE_TABLE).select("id", count="exact").in_("api_key", key_strings).gte("timestamp", yesterday).execute()
        recent_requests = recent_resp.count if recent_resp.count is not None else 0

        # 4. Daily stats (last 7 days) - aggregated in memory for simplicity
        seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat()
        daily_resp = supabase.table(API_USAGE_TABLE).select("timestamp").in_("api_key", key_strings).gte("timestamp", seven_days_ago).execute()
        
        daily_counts = {}
        if daily_resp.data:
            for record in daily_resp.data:
                date_str = record["timestamp"][:10]
                daily_counts[date_str] = daily_counts.get(date_str, 0) + 1
        
        daily_stats = [{"date": d, "count": c} for d, c in sorted(daily_counts.items())]

        return {
            "total_requests": total_requests,
            "recent_requests_24h": recent_requests,
            "key_count": len(key_strings),
            "daily_stats": daily_stats
        }
    except Exception as e:
        logger.error(f"Error fetching usage stats: {e}")
        return {
            "error": str(e),
            "total_requests": 0,
            "recent_requests_24h": 0,
            "daily_stats": []
        }
