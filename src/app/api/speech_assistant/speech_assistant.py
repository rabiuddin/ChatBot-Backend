from fastapi import APIRouter, UploadFile, File, status, Request
from src.app.models.speech_prompt import SpeechPrompt
from src.app.helper.speech_assistant.speech_assistant import process_audio
from pathlib import Path
import shutil
from datetime import datetime
from src.app.utils.response_builder_utils import ResponseBuilder
from src.app.utils.limiter_utils import limiter

speech_router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@speech_router.post("/")
@limiter.limit("30/minute")
async def getResponse(request: Request, audio_file: UploadFile = File(...)):
    response_builder = ResponseBuilder()
    try:
        # To give each file a unique name, we use the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = UPLOAD_DIR / f"{timestamp}_{audio_file.filename}"
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)
            
        request = SpeechPrompt(audio_file=str(file_path))
        response = await process_audio(request)
        
        if "error" in response:
            return response_builder.set_success(False).set_error(response["error"]).setStatusCode(status.HTTP_400_BAD_REQUEST).build()
        
        return response_builder.set_success(True).set_data(response).setStatusCode(status.HTTP_200_OK).build()
    except Exception as e:
        return response_builder.set_success(False).set_error(str(e)).setStatusCode(status.HTTP_500_INTERNAL_SERVER_ERROR).build()