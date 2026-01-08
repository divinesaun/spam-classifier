from fastapi import FastAPI
from pydantic import BaseModel
from src.parallel_analysis import run_parallel_checks
from src.llm_service import llm_scan_judgement

app = FastAPI(title="Spam Classifier")

class Message(BaseModel):
    text: str

@app.post("/detect_spam")
def detect_spam(input: Message):
    report = run_parallel_checks(input.text)
    result = llm_scan_judgement(input.text, report)
    return result