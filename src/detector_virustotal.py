import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("VIRUSTOTAL_API_KEY")

headers = {
    "x-apikey": api_key,
    "accept": "application/json"
}

base_url = "https://www.virustotal.com/api/v3/urls"

def scan_url_with_virustotal(url):
    params = {
        "url": url
    }
    if not api_key:
        return "VirusTotal API key not found in environment variables."

    response = requests.post(base_url, headers=headers, data=params)
    response.raise_for_status()
    return response.json()["data"]["id"]
