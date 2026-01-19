import dns.resolver
import logging

logger = logging.getLogger(__name__)

def dns_lookup(domain: str) -> dict:
    if not domain:
        return {"name": "dns_lookup", "error": "No domain provided"}
        
    try:
        # A records
        result_a = dns.resolver.resolve(domain, 'A')
        a_records = [ip.to_text() for ip in result_a]
        
        # NS records
        try:
            result_ns = dns.resolver.resolve(domain, 'NS')
            ns_records = [ns.to_text() for ns in result_ns]
        except:
            ns_records = []

        return {
            "name": "dns_lookup",
            "a_records": a_records,
            "ns_records": ns_records
        }
    except Exception as e:
        logger.error(f"DNS lookup failed for {domain}: {e}")
        return {"name": "dns_lookup", "error": str(e)}

def mx_lookup(domain: str) -> dict:
    if not domain:
        return {"name": "mx_lookup", "error": "No domain provided"}

    try:
        result = dns.resolver.resolve(domain, 'MX')
        mx_records = [{"exchange": r.exchange.to_text(), "priority": r.preference} for r in result]
        return {
            "name": "mx_lookup",
            "mx_records": mx_records
        }
    except Exception as e:
        logger.error(f"MX lookup failed for {domain}: {e}")
        return {"name": "mx_lookup", "error": str(e)}
