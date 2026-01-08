from concurrent.futures import ThreadPoolExecutor
from preprocess import extract_url_from_message
from detector_whois import scan_url_with_whois
from detector_virustotal import scan_url_with_virustotal
from extract_domain import extract_domain

def run_parallel_checks(message):
    url = extract_url_from_message(message)
    domain = extract_domain(url)
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        whois_results = scan_url_with_whois(domain)
        virustotal_results = scan_url_with_virustotal(domain)
    
    return {
        "url": url,
        "domain": domain,
        "whois": whois_results,
        "virustotal": virustotal_results
    }

print(run_parallel_checks("Check weather updates here: https://www.google.com"))
