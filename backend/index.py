from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from api.chatCompletion.main import router

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