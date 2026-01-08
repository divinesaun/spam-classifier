import requests
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

load_dotenv()

api_key = os.getenv("VIRUSTOTAL_API_KEY")

headers = {
    "x-apikey": api_key,
    "accept": "application/json"
}

base_url = "https://www.virustotal.com/api/v3/urls"
analysis_url = "https://www.virustotal.com/api/v3/analyses/"

def scan_url_with_virustotal(url):
    params = {
        "url": url
    }
    if not api_key:
        return "VirusTotal API key not found in environment variables."

    logging.info("Sumbitting URL to VirusTotal for analysis")
    post_response = requests.post(base_url, headers=headers, data=params)
    # post_response.raise_for_status()
    logging.info("Submission finish✔️")
    analysis_id = post_response.json()["data"]["id"]
    get_response = requests.get(f"{analysis_url}/{analysis_id}", headers=headers)
    analysis_data = get_response.json().get("data", {})
    if get_response.status_code == 200 and analysis_data:
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
            "analysis_url": f"https://www.virustotal.com/gui/url/{analysis_data.get('id')}",
            "stats": stats,
            "flagged_engines": flagged_engines
        }
    else:
        return {"error": f"Error while getting the analysis report: {get_response.status_code}"}

