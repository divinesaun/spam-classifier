import requests
from dotenv import load_dotenv
import os
import logging
logger = logging.getLogger(__name__)

load_dotenv()

api_key = os.getenv("VIRUSTOTAL_API_KEY")

headers = {
    "x-apikey": api_key,
    "accept": "application/json"
}

base_url = "https://www.virustotal.com/api/v3/urls"
analysis_url = "https://www.virustotal.com/api/v3/analyses/"

def scan_url_with_virustotal(url):
    if not url:
        return {
            "name": "VIRUSTOTAL",
            "error": "No URL provided"
        }
    
    if not api_key:
        return {
            "name": "VIRUSTOTAL",
            "error": "VirusTotal API key not found in environment variables."
        }

    params = {
        "url": url
    }

    logger.info(f"Submitting URL to VirusTotal for analysis: {url}")
    try:
        post_response = requests.post(base_url, headers=headers, data=params)
        post_response.raise_for_status()
        logger.info("Submission finish✔️")
        
        analysis_id = post_response.json().get("data", {}).get("id")
        if not analysis_id:
            return {"name": "VIRUSTOTAL", "error": "Failed to get analysis ID from VirusTotal"}

        get_response = requests.get(f"{analysis_url}/{analysis_id}", headers=headers)
        get_response.raise_for_status()
        analysis_data = get_response.json().get("data", {})

        attributes = analysis_data.get("attributes", {})
        stats = attributes.get("stats", {})
        results = attributes.get("results", {})

        # Filter to show only engines that flagged the URL as malicious or suspicious
        flagged_engines = {
            engine: details.get("result")
            for engine, details in results.items()
            if details.get("category") in ["malicious", "suspicious"]
        }

        return {
            "name": "VIRUSTOTAL",
            "analysis_url": f"https://www.virustotal.com/gui/url/{analysis_data.get('id')}",
            "stats": stats,
            "flagged_engines": flagged_engines
        }
    except Exception as e:
        logger.error(f"VirusTotal error: {e}")
        return {
            "name": "VIRUSTOTAL",
            "error": str(e)
        }