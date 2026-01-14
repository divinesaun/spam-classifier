import re

def extract_url_from_message(message):
    # Updated regex to capture URLs with or without http/https
    # Captures: http://example.com, https://example.com, www.example.com, example.com
    url_pattern = r'((?:https?://)?(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*))'
    urls = re.findall(url_pattern, message, re.IGNORECASE)
    if urls:
        # If the URL is just 'example.com', we might want to return it as is or prepend https://
        # For analysis tools like VirusTotal, 'example.com' is usually fine.
        return urls[0]
    return None
