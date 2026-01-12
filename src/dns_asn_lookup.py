import socket

def dns_asn_lookup(domain: str):
    try:
        ip = socket.gethostbyname(domain)

        return {
            "ip_address": ip,
            "resolved": True
        }
    except Exception as e:
        print(f"Error resolving domain: {e}")
        return None