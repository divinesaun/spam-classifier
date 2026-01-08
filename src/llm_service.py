import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

model = genai.GenerativeModel("gemini-2.5-flash-lite")
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
with open("./data/prompt.txt", "r") as f:
    prompt = f.read()

def llm_scan_judgement(message, report):
    response = model.generate_content(prompt.format(message=message, report=report))
    return {
        "message": message,
        "response": response.candidates[0].content.parts[0].text
    }