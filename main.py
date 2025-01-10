from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from src.app.api.chatCompletion.main import router
from src.app.api.assistant import main
from src.app.api.speechAssistant.main import speech_router

load_dotenv()

# openai.api_key = os.getenv("OPENAI_SECRET_KEY")

app = FastAPI()

# Allow CORS for frontend requests (adjust this to your frontend URL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_URLS")],  
    allow_methods=["*"],  
    allow_headers=["*"],  # Allows all headers
)

app.include_router(router, prefix="/api/chat-completion", tags=["chat-completion"])
app.include_router(main.router, prefix="/api/mergestack-assistant", tags=["assistant"])
app.include_router(speech_router, prefix="/api/speech-assistant", tags=["speech-assistant"])