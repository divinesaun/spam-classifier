import whois
from datetime import datetime, timezone
import logging
logger = logging.getLogger(__name__)

def scan_url_with_whois(domain):
    if not domain:
        return {
            "name": "WHOIS",
            "error": "No domain provided"
        }

    logger.info(f"Starting WHOIS scan for {domain}")
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
                now = datetime.now(timezone.utc)
                # If creation is naive, we might need to make it UTC-aware if we assume it's UTC
                # However, many WHOIS servers return naive datetimes in UTC.
                if creation.tzinfo is None:
                    creation = creation.replace(tzinfo=timezone.utc)
            
            age_days = (now - creation).days

        logger.info("WHOIS detection finished✔️")
        return {
            "name": "WHOIS",
            "domain_age_days": age_days,
            "registrar": getattr(w, 'registrar', None),
            "country": getattr(w, 'country', None),
            "emails": getattr(w, 'emails', None),
            "name_servers": getattr(w, 'name_servers', None),
            "expiration_date": str(w.expiration_date),
            "creation_date": str(creation),
            "is_recent_domain": (age_days is not None) and (age_days < 90),
            "has_private_registration": bool(w.get("privacy") or w.get("whois_server"))
        }

    except Exception as e:
        logger.error(f"WHOIS error for {domain}: {e}")
        return {
            "name": "WHOIS",
            "error": str(e)
        }