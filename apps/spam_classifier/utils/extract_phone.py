import re
import phonenumbers

def extract_phone_numbers(text: str) -> list[str]:
    """
    Extracts phone numbers from text using phonenumbers library.
    """
    extracted = []
    try:
        matches = phonenumbers.PhoneNumberMatcher(text, None)  # None for default region, or guess
        for match in matches:
            extracted.append(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164))
    except:
        pass
    
    # Fallback to simple regex if library fails or is too strict, though E164 above is better.
    # We will trust the library for now as it's the requested one.
    return extracted
