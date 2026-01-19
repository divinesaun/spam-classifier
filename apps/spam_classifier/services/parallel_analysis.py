import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from .detector_whois import scan_url_with_whois
from .detector_virustotal import scan_url_with_virustotal
from .lexical_analysis import lexical_analysis
from .dns_asn_lookup import dns_asn_lookup
from .tls_cert_inspection import tls_cert_inspection
from .email_checker import check_all_emails
from .dns_resolver import dns_lookup, mx_lookup
from .ip_lookup import ip_lookup
from .phone_validator import validate_all_phones
from .web_inspector import webpage_info

logger = logging.getLogger(__name__)
executor = ThreadPoolExecutor(max_workers=10)
async def run_parallel_checks(url: str, domain: str, emails: list[str] = None, phones: list[str] = None, ips: list[str] = None):
    logger.info(f"Starting parallel checks for {url}")
    loop = asyncio.get_running_loop() 
    
    tasks = []

    if url and domain:
        tasks.extend([
            loop.run_in_executor(executor, scan_url_with_whois, domain),
            loop.run_in_executor(executor, scan_url_with_virustotal, url),
            loop.run_in_executor(executor, lexical_analysis, url),
            loop.run_in_executor(executor, dns_asn_lookup, domain),
            loop.run_in_executor(executor, tls_cert_inspection, domain),
            loop.run_in_executor(executor, dns_lookup, domain),
            loop.run_in_executor(executor, mx_lookup, domain),
            loop.run_in_executor(executor, webpage_info, url)
        ])
    
    if emails:
        tasks.append(loop.run_in_executor(executor, check_all_emails, emails))

    if phones:
        tasks.append(loop.run_in_executor(executor, validate_all_phones, phones))

    if ips:
        for ip in ips:
            tasks.append(loop.run_in_executor(executor, ip_lookup, ip))
    
    # Use return_exceptions=True to avoid crashing the whole process if one task fails
    raw_results = await asyncio.gather(*tasks, return_exceptions=True)

    results = {}
    for r in raw_results:
        if isinstance(r, Exception):
            logger.error(f"Task failed with exception: {r}")
            continue
        if isinstance(r, dict) and "name" in r:
            results[r["name"]] = r
        elif r is not None:
            # Fallback for unexpected return types
            name = getattr(r, 'name', f"unknown_{type(r).__name__}")
            results[name] = r

    logger.info(f"Parallel checks completed. Successfully gathered {len(results)} results.")
    return results