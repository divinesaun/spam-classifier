import re

def extract_url_from_message(message):
    # Regex to find URLs, avoiding trailing punctuation
    url_pattern = r'(https?://[^\s<>"]+?)(?=[.,;:?!]?(?:\s|$))'
    urls = re.findall(url_pattern, message, re.IGNORECASE)
    if urls:
        return urls[0]
    return None
