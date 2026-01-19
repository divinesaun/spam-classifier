from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.responses import FileResponse
from pydantic import BaseModel
import spacy
import pickle
import os
import logging
from shared.security import verify_api_key, get_current_user
from shared.database import log_api_usage

logger = logging.getLogger(__name__)
router = APIRouter()

# Load the model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "intent_classifier_model.pkl")

nlp = None

def load_model():
    global nlp
    if not os.path.exists(MODEL_PATH):
        logger.error(f"Model file {MODEL_PATH} not found.")
        return False
    
    try:
        with open(MODEL_PATH, "rb") as f:
            nlp = pickle.load(f)
        logger.info(f"Intent model loaded from {MODEL_PATH}")
        return True
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        return False

# Load on module import
load_model()

class ClassifyRequest(BaseModel):
    text: str

class ClassifyResponse(BaseModel):
    text: str
    intent: str
    confidence: float

@router.post("/classify", response_model=ClassifyResponse)
async def classify_intent(
    request: ClassifyRequest, 
    api_key: dict = Security(verify_api_key)
):
    """
    Classifies the intent of a text string.
    Requires a valid X-API-Key in the header.
    """
    if nlp is None:
        if not load_model():
            raise HTTPException(status_code=500, detail="Model not initialized.")
    
    try:
        doc = nlp(request.text)
        intent_scores = doc.cats
        if not intent_scores:
            raise HTTPException(status_code=500, detail="Model returned no scores.")
        
        best_intent = max(intent_scores, key=intent_scores.get)
        confidence = intent_scores[best_intent]
        
        # Log usage if it's a specific key (not master or dict)
        if isinstance(api_key, dict) and 'id' in api_key:
            await log_api_usage(api_key['id'], "/intent/classify")
        
        return ClassifyResponse(
            text=request.text,
            intent=best_intent,
            confidence=confidence
        )
    except Exception as e:
        logger.error(f"Classification error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download-model")
async def download_model(user = Depends(get_current_user)):
    """
    Allows authenticated users to download the trained .pkl model file.
    Requires a valid Supabase JWT (Bearer Token).
    """
    if not os.path.exists(MODEL_PATH):
        raise HTTPException(status_code=404, detail="Model file not found.")
    
    return FileResponse(
        path=MODEL_PATH,
        filename="intent_classifier_model.pkl",
        media_type="application/octet-stream"
    )

