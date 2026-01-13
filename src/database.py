import os
import logging
import json
from datetime import datetime
from supabase import create_client, Client
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

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

TABLE_NAME = "scam_analysis"

async def check_url_in_db(url: str) -> Optional[Dict[str, Any]]:
    """
    Checks if the URL exists in the database.
    Returns the record if found, else None.
    """
    if not supabase:
        return None

    try:
        response = supabase.table(TABLE_NAME).select("*").eq("url", url).execute()
        if response.data and len(response.data) > 0:
            logger.info(f"URL found in database: {url}")
            return response.data[0]
    except Exception as e:
        logger.error(f"Error checking URL in database: {e}")
    
    return None

async def save_analysis_result(url: str, domain: str, report: Dict[str, Any], verdict: str, score: int = 0):
    """
    Saves the analysis result to the database.
    """
    if not supabase:
        return

    data = {
        "url": url,
        "domain": domain,
        "full_report": report,
        "verdict": verdict,
        "risk_score": score,
        "created_at": datetime.now().isoformat()
    }

    try:
        # Upsert allows updating if it already exists (though check_url_in_db should catch it first)
        supabase.table(TABLE_NAME).upsert(data).execute()
        logger.info(f"Saved analysis for {url} to database.")
    except Exception as e:
        logger.error(f"Error saving to database: {e}")

async def get_api_key(key_value: str):
    """
    Validates an API key against the database (if we store keys there) or env.
    For this task, we can just check if it exists in a specific 'api_keys' table
    or just return True for now if not implementing full key management yet.
    """
    if not supabase:
        return None # or handle as strictly env based
    
    try:
        response = supabase.table("api_keys").select("*").eq("key", key_value).eq("is_active", True).execute()
        if response.data:
            return response.data[0]
    except Exception as e:
        logger.error(f"Error validating API key: {e}")
    
    return None
