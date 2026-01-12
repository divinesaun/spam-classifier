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

@app.post("/webhook")
async def whatsapp_webhook(Body: str = Form(...)):
    """
    Twilio Webhook for WhatsApp.
    Receives the message body, runs spam detection, and replies with the result.
    """
    logger.info(f"Incoming WhatsApp message: {Body}")
    
    analysis_result = await analyze_message(Body)
    response_text = analysis_result.get("response", "Could not analyze message.")
    
    # Create Twilio XML response
    resp = MessagingResponse()
    resp.message(response_text)
    
    return Response(content=str(resp), media_type="application/xml")