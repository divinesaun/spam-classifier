import re

def extract_emails_from_message(message: str) -> list[str]:
    """
    Extracts all email addresses from a given message string.
    """
    # Regex pattern for email extraction
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, message)
    return emails
