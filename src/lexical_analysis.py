import re
from urllib.parse import urlparse

SUSPICIOUS_KEYWORDS = [
    "verify", "login", "secure", "update",
    "payment", "confirm", "account", "win",
    "click", "claim", "prize", "winner",
    "urgent", "alert", "warning", "error",
    "expired",
]

def url_lexical_analysis(url: str):
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname or ""

        subdomains = hostname.split(".")[:-2]
        path = parsed.path.lower()

        features = {
            "name": "lexical_analysis",
            "length": len(url),
            "num_subdomains": len(subdomains),
            "has_ip": bool(re.search(r"\d+\.\d+\.d+\.\d+", hostname)),
            "suspicious_keywords": [k for k in SUSPICIOUS_KEYWORDS if k in url.lower()],
            "has_url_shortener": bool(re.search(r"(bit\.ly|tinyurl|ow\.ly|is\.gd|bitly|t\.co|short\.ly|tinyurl|tr\.im|bit\.ly|ow\.ly|is\.gd|bitly|t\.co|short\.ly|tinyurl|tr\.im|bit\.ly|ow\.ly|is\.gd|bitly|t\.co|short\.ly|tinyurl|tr\.im)", url)),
        }

        return features
    except Exception as e:
        print(f"Error processing URL: {e}")
        return None