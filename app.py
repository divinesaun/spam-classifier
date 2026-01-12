import logging
import json

# Configure logging centrally at the very top
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    force=True
)
logger = logging.getLogger(__name__)

from fastapi import FastAPI, Form, Response
from pydantic import BaseModel
from src.parallel_analysis import run_parallel_checks
from src.llm_service import llm_scan_judgement
from src.extract_url import extract_url_from_message
from src.extract_domain import extract_domain_from_url
from twilio.twiml.messaging_response import MessagingResponse

app = FastAPI(title="Spam Classifier")

class Message(BaseModel):
    text: str

async def analyze_message(text: str):
    logger.info(f"Analyzing text: {text[:50]}...")
    
    url = extract_url_from_message(text)
    domain = extract_domain_from_url(url) if url else None
    
    if url and domain:
        logger.info(f"Analyzing URL: {url} (Domain: {domain})")
        report = await run_parallel_checks(url, domain)
    else:
        logger.warning("No URL found in message, skipping deep analysis")
        report = {"info": "No URL found in message for deep analysis"}
        
    # Print information given to the LLM
    print("\n" + "="*50)
    print("DATA SENT TO LLM:")
    print(json.dumps(report, indent=2))
    print("="*50 + "\n")
    
    logger.info("Requesting judgment from LLM...")
    result = llm_scan_judgement(text, report)
    logger.info("Spam analysis complete.")
    
    return result

@app.post("/detect_spam")
async def detect_spam(input: Message):
    logger.info(f"Incoming request: {input.text[:50]}...")
    return await analyze_message(input.text)

from src.ocr_service import extract_text_from_image

@app.post("/webhook")
async def whatsapp_webhook(
    Body: str = Form(""),
    NumMedia: int = Form(0),
    MediaUrl0: str = Form(None)
):
    """
    Twilio Webhook for WhatsApp.
    Receives the message body and media. 
    If an image is present, it uses OCR to extract text.
    Then runs spam detection on the combined text and replies with the result.
    """
    logger.info(f"Incoming WhatsApp message. Body: {Body}, NumMedia: {NumMedia}")
    
    analyzed_text = Body
    
    # Check for image and run OCR if available
    if NumMedia > 0 and MediaUrl0:
        logger.info(f"Media detected. URL: {MediaUrl0}")
        ocr_text = await extract_text_from_image(MediaUrl0)
        if ocr_text:
            logger.info(f"OCR extracted text: {ocr_text[:50]}...")
            # Append OCR text to the user's message
            analyzed_text = f"{Body}\n\n[OCR EXTRACTED CONTENT]:\n{ocr_text}"
        else:
            logger.warning("OCR failed to extract text or API error.")

    analysis_result = await analyze_message(analyzed_text)
    response_text = analysis_result.get("response", "Could not analyze message.")
    
    # Create Twilio XML response
    resp = MessagingResponse()
    resp.message(response_text)
    
    return Response(content=str(resp), media_type="application/xml")