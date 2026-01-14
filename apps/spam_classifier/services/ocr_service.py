import requests
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

OCR_API_KEY = os.getenv("OCR_SPACE_API_KEY")

async def extract_text_from_image(image_url):
    """
    Uses OCR.space API to extract text from an image URL.
    """
    if not OCR_API_KEY:
        logger.error("OCR_SPACE_API_KEY not found in environment variables.")
        return None

    api_url = "https://api.ocr.space/parse/image"

    try:
        payload = {
            "apikey": OCR_API_KEY,
            "url": image_url,
            "language": "eng",
            "isOverlayRequired": False,
        }
        
        logger.info(f"Sending image to OCR.space: {image_url}")
        response = requests.post(api_url, data=payload)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get("IsErroredOnProcessing"):
            error_message = result.get("ErrorMessage")
            logger.error(f"OCR API Error: {error_message}")
            return None
            
        parsed_results = result.get("ParsedResults")
        if parsed_results:
            extracted_text = parsed_results[0].get("ParsedText")
            logger.info("OCR Extraction successful.")
            return extracted_text
        else:
            logger.warning("No text found in OCR response.")
            return ""

    except Exception as e:
        logger.error(f"Error occurring during OCR extraction: {e}")
        return None
