from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile

class SpeechPrompt(BaseModel):
    audio_file: str