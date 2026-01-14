
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
async def detect_spam(request: Request, input: Message, api_key: str = Depends(verify_api_key)):
    logger.info(f"Incoming request: {input.text[:50]}...")
    return await analyze_message_logic(input.text)

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
