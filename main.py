
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from shared.limiter import limiter
from apps.spam_classifier.router import router as spam_router
from apps.content_moderator.router import router as moderator_router
from apps.auth.router import router as auth_router


# Configure logging centrally
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    force=True
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Unified AI Backend")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- CORS Configuration ---
origins = [
    "http://localhost:3000",
    "http://localhost:5173", 
    "*" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include Routers ---
app.include_router(spam_router, prefix="/spam", tags=["Spam Classifier"])
app.include_router(moderator_router, prefix="/moderator", tags=["Content Moderator"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Unified AI Backend. Access apps via their respective paths."}
