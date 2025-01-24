from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from src.app.api.chat_completion import chat_completion
from src.app.api.assistant import assistant
from src.app.api.speech_assistant import speech_assistant
from src.app.api.chats import chats
from src.app.api.chats import messages
from slowapi.errors import RateLimitExceeded
from src.app.utils.limiter_utils import limiter,  rate_limit_exceeded_handler

load_dotenv()

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

cors_urls = os.getenv("CORS_URLS", "").split(",")

# Allow CORS for frontend requests (adjust this to your frontend URL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_urls, 
    allow_methods=["*"],  
    allow_headers=["*"],  # Allows all headers
)


app.include_router(chat_completion.router, prefix="/api/chat-completion", tags=["chat-completion"])
app.include_router(assistant.router, prefix="/api/mergestack-assistant", tags=["assistant"])
app.include_router(speech_assistant.speech_router, prefix="/api/speech-assistant", tags=["speech-assistant"])
app.include_router(chats.router, prefix="/api/chats", tags=["chats"])
app.include_router(messages.router, prefix="/api/messages", tags=["messages"])
