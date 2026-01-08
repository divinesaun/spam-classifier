from concurrent.futures import ThreadPoolExecutor
from extract_url import extract_url_from_message
from detector_whois import scan_url_with_whois
from detector_virustotal import scan_url_with_virustotal
from extract_domain import extract_domain_from_url

def run_parallel_checks(message):
    url = extract_url_from_message(message)
    domain = extract_domain_from_url(url)
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        whois_results = scan_url_with_whois(domain)
        virustotal_results = scan_url_with_virustotal(url)
    
    return {
        "url": url,
        "domain": domain,
        "whois": whois_results,
        "virustotal": virustotal_results
    }