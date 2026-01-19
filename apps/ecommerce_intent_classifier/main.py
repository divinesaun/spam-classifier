from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import spacy
import pickle
import os

app = FastAPI(title="Ecommerce Intent Classifier API")

# Load the model
MODEL_PATH = "intent_classifier_model.pkl"

if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"Model file {MODEL_PATH} not found. Please run training script first.")

with open(MODEL_PATH, "rb") as f:
    nlp = pickle.load(f)

class ClassifyRequest(BaseModel):
    text: str

class ClassifyResponse(BaseModel):
    text: str
    intent: str
    confidence: float

@app.post("/classify", response_model=ClassifyResponse)
async def classify_intent(request: ClassifyRequest):
    try:
        doc = nlp(request.text)
        # Get the label with the highest score
        intent_scores = doc.cats
        if not intent_scores:
            raise HTTPException(status_code=500, detail="Model returned no scores.")
        
        best_intent = max(intent_scores, key=intent_scores.get)
        confidence = intent_scores[best_intent]
        
        return ClassifyResponse(
            text=request.text,
            intent=best_intent,
            confidence=confidence
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Ecommerce Intent Classifier API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
