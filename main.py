from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from src.app.api.chat_completion import chat_completion
from src.app.api.assistant import assistant
from src.app.api.speech_assistant import speech_assistant
from slowapi.errors import RateLimitExceeded
from src.app.utils.limiter_utils import limiter,  rate_limit_exceeded_handler

load_dotenv()

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)


# Allow CORS for frontend requests (adjust this to your frontend URL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_URLS")],  
    allow_methods=["*"],  
    allow_headers=["*"],  # Allows all headers
)


app.include_router(chat_completion.router, prefix="/api/chat-completion", tags=["chat-completion"])
app.include_router(assistant.router, prefix="/api/mergestack-assistant", tags=["assistant"])
app.include_router(speech_assistant.speech_router, prefix="/api/speech-assistant", tags=["speech-assistant"])