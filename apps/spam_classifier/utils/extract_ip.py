import re

def extract_ips_from_message(message: str) -> list[str]:
    # Extract IPv4 addresses
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    ips = re.findall(ip_pattern, message)
    # Basic validation to ensure octets are 0-255
    valid_ips = []
    for ip in ips:
        parts = ip.split('.')
        if all(0 <= int(part) <= 255 for part in parts):
            valid_ips.append(ip)
    return valid_ips
