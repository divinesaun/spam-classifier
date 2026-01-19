import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def webpage_info(url: str) -> dict:
    if not url:
        return {"name": "webpage_info", "error": "No URL provided"}

    try:
        # Default header to avoid some 403s
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        r = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        title = soup.title.string if soup.title else None
        
        description_tag = soup.find("meta", attrs={"name": "description"})
        description = description_tag["content"] if description_tag else None
        
        # Also grab h1s as per web_scraper suggestion
        h1s = [el.get_text(strip=True) for el in soup.select("h1")]

        return {
            "name": "webpage_info",
            "url": url,
            "title": title,
            "description": description,
            "h1_tags": h1s
        }
    except Exception as e:
        logger.error(f"Web page info failed for {url}: {e}")
        return {"name": "webpage_info", "error": str(e)}
