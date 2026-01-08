import whois
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def scan_url_with_whois(domain):
    logging.info("Starting WHOIS scan")
    try:

        w = whois.whois(domain)
        creation = w.creation_date
        if isinstance(creation, list):
            creation = creation[0]

        age_days = None
        if creation:
            age_days = (datetime.utcnow() - creation).days

        return {
            "source": "WHOIS",
            "domain_age_days": age_days,
            "registrar": w.registrar,
            "country": w.country,
            "is_recent_domain": (age_days != None) and (age_days < 90),
            "has_private_registration": bool(w.get("privacy") or w.get("whois_server"))
        }

    except Exception as e:
        return {
            "source": "WHOIS",
            "error": str(e)
        }