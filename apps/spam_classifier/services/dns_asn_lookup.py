import socket
import logging

logger = logging.getLogger(__name__)

def dns_asn_lookup(domain: str):
    logger.info(f"Starting DNS lookup for: {domain}")
    try:
        ip = socket.gethostbyname(domain)
        logger.info(f"DNS lookup successful: {ip}")
        return {
            "name": "dns_asn_lookup",
            "ip_address": ip,
            "resolved": True
        }
    except Exception as e:
        logger.error(f"DNS lookup error for {domain}: {e}")
        return {
            "name": "dns_asn_lookup",
            "error": str(e)
        }