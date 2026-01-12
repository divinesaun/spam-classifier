from concurrent.futures import ThreadPoolExecutor
from src.extract_url import extract_url_from_message
from src.detector_whois import scan_url_with_whois
from src.detector_virustotal import scan_url_with_virustotal
from src.extract_domain import extract_domain_from_url
from src.lexical_analysis import lexical_analysis
from dns_asn_lookup import dns_asn_lookup
from tls_cert_inspection import tls_cert_inspection
import asyncio

executor = ThreadPoolExecutor(max_workers=6)
async def run_parallel_checks(url, domain):
    loop = asyncio.get_running_loop() 

    tasks = [
        loop.run_in_executor(executor, scan_url_with_whois, domain),
        loop.run_in_executor(executor, scan_url_with_virustotal, url),
        loop.run_in_executor(executor, lexical_analysis, url),
        loop.run_in_executor(executor, dns_asn_lookup, domain),
        loop.run_in_executor(executor, tls_cert_inspection, domain)
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=False)

    return {r.name: r for r in results}