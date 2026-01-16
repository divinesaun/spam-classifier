
import logging
from fastapi import APIRouter, Form, Response, Depends, Request
from pydantic import BaseModel
from shared.limiter import limiter
from shared.security import verify_api_key
from .orchestrator import analyze_message_logic, extract_text_from_image, AnalysisResult
from twilio.twiml.messaging_response import MessagingResponse

router = APIRouter()
logger = logging.getLogger(__name__)

class Message(BaseModel):
    text: str

@router.post("/detect_spam", response_model=AnalysisResult)
@limiter.limit("5/minute")
async def detect_spam(request: Request, input: Message, api_key_data = Depends(verify_api_key)):
    logger.info(f"Incoming request: {input.text[:50]}...")
    
    result = await analyze_message_logic(input.text)
    
    # Log usage if it's a database key (not master key)
    if isinstance(api_key_data, dict) and "key" in api_key_data:
        from shared.database import log_api_usage
        await log_api_usage(
            api_key=api_key_data["key"],
            endpoint="/detect_spam",
            method="POST",
            status_code=200
        )
    
    return result

@router.post("/webhook")
async def whatsapp_webhook(
    Body: str = Form(""),
    NumMedia: int = Form(0),
    MediaUrl0: str = Form(None)
):
    logger.info(f"Incoming WhatsApp message. Body: {Body}, NumMedia: {NumMedia}")
    
    analyzed_text = Body
    
    if NumMedia > 0 and MediaUrl0:
        logger.info(f"Media detected. URL: {MediaUrl0}")
        ocr_text = await extract_text_from_image(MediaUrl0)
        if ocr_text:
            logger.info(f"OCR extracted text: {ocr_text[:50]}...")
            analyzed_text = f"{Body}\n\n[OCR EXTRACTED CONTENT]:\n{ocr_text}"

    result = await analyze_message_logic(analyzed_text)
    
    resp = MessagingResponse()
    resp.message(result.response_text)
    return Response(content=str(resp), media_type="application/xml")
