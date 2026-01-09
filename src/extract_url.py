import re

def extract_url_from_message(message):
    url_pattern = r'(https?://[^\s]+)'
    urls = re.findall(url_pattern, message)
    if len(urls) > 0:
        return urls[0]
    else:
        return None
