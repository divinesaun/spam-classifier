from google import genai
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)
load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
prompt_path = os.path.join(BASE_DIR, "data", "prompt.txt")

with open(prompt_path, "r") as f:
    prompt = f.read()

def llm_scan_judgement(message, report):
    logger.info("Sending prompt and report to LLM for judgment")
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt.format(message=message, report=report)
        )
        return {
            "message": message,
            "response": response.text
        }
    except Exception as e:
        return {
            "message": message,
            "response": f"Error: {str(e)}"
        }