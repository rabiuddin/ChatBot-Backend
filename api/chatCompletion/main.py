from fastapi import APIRouter
from dotenv import load_dotenv
import os
from api.chatCompletion import openai, gemini

load_dotenv()

router = APIRouter()

router.include_router(openai.router, prefix="/openai", tags=["openai"])
router.include_router(gemini.router, prefix="/gemini", tags=["gemini"])