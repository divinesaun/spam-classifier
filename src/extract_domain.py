import tldextract

def extract_domain_from_url(url):
    if url:
        ext = tldextract.extract(url)
        return f"{ext.domain}.{ext.suffix}"
    else:
        return None