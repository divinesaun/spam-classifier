import os
import logging

logger = logging.getLogger(__name__)

BLOCKLIST_PATH = os.path.join(os.getcwd(), 'data', 'disposable_email_blocklist.txt')

_disposable_domains = set()

def _load_blocklist():
    global _disposable_domains
    if _disposable_domains:
        return

    if not os.path.exists(BLOCKLIST_PATH):
        logger.warning(f"Blocklist file not found at {BLOCKLIST_PATH}")
        return

    try:
        with open(BLOCKLIST_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                domain = line.strip().lower()
                if domain:
                    _disposable_domains.add(domain)
        logger.info(f"Loaded {len(_disposable_domains)} disposable domains.")
    except Exception as e:
        logger.error(f"Failed to load disposable email blocklist: {e}")

def check_disposable_email(email: str) -> dict:
    _load_blocklist()
    
    if not email:
         return {
            "name": "disposable_email_check",
            "email": email,
            "error": "No email provided"
        }

    try:
        domain = email.split('@')[-1].strip().lower()
        is_disposable = domain in _disposable_domains
        
        return {
            "name": "disposable_email_check",
            "email": email,
            "domain": domain,
            "is_disposable": is_disposable,
        }
    except Exception as e:
        logger.error(f"Error checking email {email}: {e}")
        return {
            "name": "disposable_email_check",
            "email": email,
            "error": str(e)
        }

def check_all_emails(emails: list[str]) -> dict:
    results = []
    for email in emails:
        results.append(check_disposable_email(email))
    
    # Aggregate verdict
    any_disposable = any(r.get("is_disposable", False) for r in results)
    
    return {
        "name": "email_analysis",
        "found_emails": len(emails),
        "results": results,
        "any_disposable": any_disposable
    }
