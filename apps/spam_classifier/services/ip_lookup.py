import requests
import logging

logger = logging.getLogger(__name__)

def ip_lookup(ip: str) -> dict:
    if not ip:
        return {"name": "ip_lookup", "error": "No IP provided"}

    try:
        # Using ip-api.com as requested
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "name": "ip_lookup",
                "ip": ip,
                "data": data
            }
        else:
            return {"name": "ip_lookup", "error": f"Status {response.status_code}"}
    except Exception as e:
        logger.error(f"IP lookup failed for {ip}: {e}")
        return {"name": "ip_lookup", "error": str(e)}
