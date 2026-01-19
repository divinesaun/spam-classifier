import requests
import json
import os

# Default to local unified backend path
BASE_URL = os.environ.get("API_URL", "http://localhost:8000")
url = f"{BASE_URL}/intent/classify"

payload = {"text": "I want to buy some red t-shirts"}
headers = {
    "Content-Type": "application/json",
    "X-API-Key": os.environ.get("MASTER_API_KEY", "your_master_key_here")
}

print(f"Testing against: {url}")

try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")

