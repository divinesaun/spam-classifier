
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from shared.database import supabase

logger = logging.getLogger(__name__)

TABLE_NAME = "scam_analysis"

async def check_url_in_db(url: str) -> Optional[Dict[str, Any]]:
    if not supabase: return None
    try:
        response = supabase.table(TABLE_NAME).select("*").eq("url", url).execute()
        if response.data and len(response.data) > 0:
            logger.info(f"URL found in database: {url}")
            return response.data[0]
    except Exception as e:
        logger.error(f"Error checking URL in database: {e}")
    return None

async def save_analysis_result(url: str, domain: str, report: Dict[str, Any], verdict: str, score: int = 0):
    if not supabase: return
    data = {
        "url": url,
        "domain": domain,
        "full_report": report,
        "verdict": verdict,
        "risk_score": score,
        "created_at": datetime.now().isoformat()
    }
    try:
        supabase.table(TABLE_NAME).upsert(data).execute()
        logger.info(f"Saved analysis for {url} to database.")
    except Exception as e:
        logger.error(f"Error saving to database: {e}")
