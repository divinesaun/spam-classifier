from concurrent.futures import ThreadPoolExecutor
from src.extract_url import extract_url_from_message
from src.detector_whois import scan_url_with_whois
from src.detector_virustotal import scan_url_with_virustotal
from src.extract_domain import extract_domain_from_url

def run_parallel_checks(message):
    url = extract_url_from_message(message)
    domain = extract_domain_from_url(url)

    if url or domain:
        with ThreadPoolExecutor(max_workers=2) as executor:
            whois_results = scan_url_with_whois(domain)
            virustotal_results = scan_url_with_virustotal(url)
        
        return {
            "url": url,
            "domain": domain,
            "whois": whois_results,
            "virustotal": virustotal_results
        }
    else:
        return {
            "response": "No report found"
        }