import whois
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def scan_url_with_whois(domain):
    if domain:
        logging.info("Starting WHOIS scan")
        try:

            w = whois.whois(domain)
            creation = w.creation_date
            if isinstance(creation, list):
                creation = creation[0]

            age_days = None
            if creation:
                # Handle timezone-aware vs naive datetimes
                if creation.tzinfo:
                    now = datetime.now(creation.tzinfo)
                else:
                    now = datetime.utcnow()
                age_days = (now - creation).days

            logging.info("WHOIS detection finished✔️")
            return {
                "name": "WHOIS",
                "domain_age_days": age_days,
                "registrar": w.registrar,
                "country": w.country,
                "is_recent_domain": (age_days != None) and (age_days < 90),
                "has_private_registration": bool(w.get("privacy") or w.get("whois_server"))
            }

        except Exception as e:
            logging.error(e)
            return {
                "name": "WHOIS",
                "error": str(e)
            }
    else:
        return None