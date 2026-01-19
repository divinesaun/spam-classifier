import phonenumbers
import logging

logger = logging.getLogger(__name__)

def validate_phone(number: str, region=None) -> dict:
    if not number:
        return {"name": "phone_validation", "error": "No number provided"}

    try:
        parsed = phonenumbers.parse(number, region)
        is_valid = phonenumbers.is_valid_number(parsed)
        
        return {
            "name": "phone_validation",
            "number": number,
            "valid": is_valid,
            "international_format": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL) if is_valid else None,
            "country": phonenumbers.region_code_for_number(parsed) if is_valid else None
        }
    except Exception as e:
        logger.error(f"Phone validation failed for {number}: {e}")
        return {"name": "phone_validation", "error": str(e)}

def validate_all_phones(numbers: list[str]) -> dict:
    results = []
    for num in numbers:
        results.append(validate_phone(num))
    return {
        "name": "phone_analysis",
        "found_numbers": len(numbers),
        "results": results
    }
