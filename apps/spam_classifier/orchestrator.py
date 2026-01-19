
import logging
from .services.parallel_analysis import run_parallel_checks
from .services.llm_service import llm_scan_judgement
from .utils.extract_url import extract_url_from_message
from .utils.extract_email import extract_emails_from_message
from .utils.extract_domain import extract_domain_from_url
from .utils.extract_phone import extract_phone_numbers
from .utils.extract_ip import extract_ips_from_message
from .services.ocr_service import extract_text_from_image
from .repository import check_url_in_db, save_analysis_result
from pydantic import BaseModel

logger = logging.getLogger(__name__)

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
    """
    verdict = "UNKNOWN"
    score = 50 
    
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
    emails = extract_emails_from_message(text)
    phones = extract_phone_numbers(text)
    ips = extract_ips_from_message(text)
    
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
            verdict = db_record.get('verdict', 'UNKNOWN')
            score = db_record.get('risk_score', 0)
            llm_response_text = f"*Verdict*: {verdict}\n*Risk Level*: {'High' if score > 70 else 'Low'}\n*Previously Analysis*: Previously analyzed as {verdict.lower()}."
             
            return AnalysisResult(
                url=url,
                domain=domain,
                verdict=verdict,
                risk_score=score,
                response_text=llm_response_text,
                full_report=db_record.get('full_report')
            )

    # 2. Run Analysis if not in DB
    if (url and domain) or emails or phones or ips:
        logger.info(f"Analyzing: URL={url}, Emails={len(emails)}, Phones={len(phones)}, IPs={len(ips)}")
        report = await run_parallel_checks(url, domain, emails, phones, ips)
    else:
        logger.warning("No analyzable entities found in message, skipping deep analysis")
        report = {"info": "No URL, emails, phones, or IPs found in message for deep analysis"}
        
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
