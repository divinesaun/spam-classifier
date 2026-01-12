import re
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

SUSPICIOUS_KEYWORDS = [
    "verify", "login", "secure", "update",
    "payment", "confirm", "account", "win",
    "click", "claim", "prize", "winner",
    "urgent", "alert", "warning", "error",
    "expired",
]

def lexical_analysis(url: str):
    logger.info(f"Starting lexical analysis for: {url}")
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname or ""

        # Basic subdomain count
        parts = hostname.split(".")
        subdomains = parts[:-2] if len(parts) > 2 else []

        features = {
            "name": "lexical_analysis",
            "length": len(url),
            "num_subdomains": len(subdomains),
            "has_ip": bool(re.search(r"\d+\.\d+\.\d+\.\d+", hostname)),
            "suspicious_keywords": [k for k in SUSPICIOUS_KEYWORDS if k in url.lower()],
            "has_url_shortener": bool(re.search(r"(bit\.ly|tinyurl|ow\.ly|is\.gd|bitly|t\.co|short\.ly|tr\.im)", url.lower())),
        }

        logger.info("Lexical analysis successful")
        return features
    except Exception as e:
        logger.error(f"Lexical analysis error: {e}")
        return {
            "name": "lexical_analysis",
            "error": str(e)
        }