import ssl
import socket
import logging

logger = logging.getLogger(__name__)

def tls_cert_inspection(domain: str):
    logger.info(f"Starting TLS certificate inspection for: {domain}")
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
        
        logger.info("TLS certificate inspection successful")
        return {
            "name": "tls_cert_inspection",
            "issuer": dict(x[0] for x in cert.get("issuer", [])),
            "subject": dict(x[0] for x in cert.get("subject", [])),
            "not_before": cert.get("notBefore", ""),
            "not_after": cert.get("notAfter", "")
        }
    except Exception as e:
        logger.error(f"TLS certificate inspection error for {domain}: {e}")
        return {
            "name": "tls_cert_inspection",
            "error": str(e)
        }