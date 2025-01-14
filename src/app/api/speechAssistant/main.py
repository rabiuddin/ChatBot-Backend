from fastapi import APIRouter, UploadFile, File
from src.app.models.speech_prompt import SpeechPrompt
from src.app.helper.speech_assistant_helper.speech_assistant import process_audio
from pathlib import Path
import shutil
from datetime import datetime
from src.app.utils.encryption import encrypt

speech_router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@speech_router.post("/")
async def getResponse(audio_file: UploadFile = File(...)):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = UPLOAD_DIR / f"{timestamp}_{audio_file.filename}"
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(audio_file.file, buffer)
        
    request = SpeechPrompt(audio_file=str(file_path))
    response = await process_audio(request)
    return {"data": encrypt(response)}