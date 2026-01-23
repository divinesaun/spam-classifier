import google.generativeai as genai
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)
load_dotenv()

model = genai.GenerativeModel("gemini-2.5-flash-lite")
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
prompt_path = os.path.join(BASE_DIR, "data", "prompt.txt")



def llm_scan_judgement(message, report):
    logger.info("Sending prompt and report to LLM for judgment")
    try:
        if not os.path.exists(prompt_path):
             return {
                "message": message,
                "response": "Error: Prompt file not found."
            }
            
        with open(prompt_path, "r") as f:
            prompt = f.read()
            
        response = model.generate_content(prompt.format(message=message, report=report))
        return {
            "message": message,
            "response": response.candidates[0].content.parts[0].text
        }
    except Exception as e:
        return {
            "message": message,
            "response": f"Error: {str(e)}"
        }