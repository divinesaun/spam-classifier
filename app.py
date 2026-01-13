import logging
import json
import asyncio
from fastapi import FastAPI, Form, Response, Depends, Request
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from src.parallel_analysis import run_parallel_checks
from src.llm_service import llm_scan_judgement
from src.extract_url import extract_url_from_message
from src.extract_domain import extract_domain_from_url
from src.ocr_service import extract_text_from_image
from src.database import check_url_in_db, save_analysis_result
from src.security import verify_api_key
from twilio.twiml.messaging_response import MessagingResponse

# Configure logging centrally at the very top
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    force=True
)
logger = logging.getLogger(__name__)

# Rate Limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Spam Classifier")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

class Message(BaseModel):
    text: str

class AnalysisResult(BaseModel):
    url: str | None
    domain: str | None
    verdict: str
    risk_score: int
    response_text: str
    full_report: dict | None

def parse_llm_response(response_text: str):
    """
    Simple parser to extract verdict and score from LLM text response.
    Expects format like "Verdict: SCAM-LIKELY" or "Verdict: SAFE"
    """
    verdict = "UNKNOWN"
    score = 50 # Default to medium risk
    
    upper_text = response_text.upper()
    
    if "SCAM-LIKELY" in upper_text:
        verdict = "SCAM"
        score = 90
    elif "SAFE" in upper_text:
        verdict = "SAFE"
        score = 10
        
    if "RISK LEVEL: HIGH" in upper_text:
        score = max(score, 80)
    elif "RISK LEVEL: LOW" in upper_text:
        score = min(score, 20)
        
    return verdict, score

async def analyze_message_logic(text: str) -> AnalysisResult:
    logger.info(f"Analyzing text: {text[:50]}...")
    
    url = extract_url_from_message(text)
    domain = extract_domain_from_url(url) if url else None
    
    report = {}
    verdict = "UNKNOWN"
    score = 0
    llm_response_text = ""

    # 1. Check Database First
    if url:
        logger.info(f"Checking database for URL: {url}")
        db_record = await check_url_in_db(url)
        if db_record:
            logger.info("URL found in database. Returning cached result.")
            # Construct response from DB record
            # We assume the DB record stores the structured report and a generic response or we regenerate it?
            # The user said "return the response". Creating a summary from DB data.
            verdict = db_record.get('verdict', 'UNKNOWN')
            score = db_record.get('risk_score', 0)
            llm_response_text = f"*Verdict*: {verdict}\n*Risk Level*: {'High' if score > 70 else 'Low'}\n*Advice*: previously analyzed as {verdict.lower()}."
             
            return AnalysisResult(
                url=url,
                domain=domain,
                verdict=verdict,
                risk_score=score,
                response_text=llm_response_text,
                full_report=db_record.get('full_report')
            )

    # 2. Run Analysis if not in DB
    if url and domain:
        logger.info(f"Analyzing URL: {url} (Domain: {domain})")
        report = await run_parallel_checks(url, domain)
    else:
        logger.warning("No URL found in message, skipping deep analysis")
        report = {"info": "No URL found in message for deep analysis"}
        
    # 3. LLM Judgement
    logger.info("Requesting judgment from LLM...")
    llm_result = llm_scan_judgement(text, report)
    llm_response_text = llm_result.get("response", "Could not analyze message.")
    
    # 4. Parse Verdict
    verdict, score = parse_llm_response(llm_response_text)
    
    # 5. Save to Database
    if url:
        await save_analysis_result(url, domain, report, verdict, score)
    
    return AnalysisResult(
        url=url,
        domain=domain,
        verdict=verdict,
        risk_score=score,
        response_text=llm_response_text,
        full_report=report
    )

@app.post("/detect_spam", response_model=AnalysisResult)
@limiter.limit("5/minute")
async def detect_spam(request: Request, input: Message, api_key: str = Depends(verify_api_key)):
    logger.info(f"Incoming request: {input.text[:50]}...")
    return await analyze_message_logic(input.text)

@app.post("/webhook")
async def whatsapp_webhook(
    Body: str = Form(""),
    NumMedia: int = Form(0),
    MediaUrl0: str = Form(None)
):
    """
    Twilio Webhook for WhatsApp.
    """
    logger.info(f"Incoming WhatsApp message. Body: {Body}, NumMedia: {NumMedia}")
    
    analyzed_text = Body
    
    if NumMedia > 0 and MediaUrl0:
        logger.info(f"Media detected. URL: {MediaUrl0}")
        ocr_text = await extract_text_from_image(MediaUrl0)
        if ocr_text:
            logger.info(f"OCR extracted text: {ocr_text[:50]}...")
            analyzed_text = f"{Body}\n\n[OCR EXTRACTED CONTENT]:\n{ocr_text}"
        else:
            logger.warning("OCR failed to extract text or API error.")

    result = await analyze_message_logic(analyzed_text)
    
    resp = MessagingResponse()
    resp.message(result.response_text)
    
    return Response(content=str(resp), media_type="application/xml")