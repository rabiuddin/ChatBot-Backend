import assemblyai as aai
from src.app.config import Config
from src.app.models.speech_prompt import SpeechPrompt
import os

config = Config()
aai.settings.api_key = config.get_assemblyai_api_key()

async def process_audio(request: SpeechPrompt):
    try:
        transcriber = aai.Transcriber()

        transcript = transcriber.transcribe(request.audio_file)

        os.remove(request.audio_file)

        if transcript.status == aai.TranscriptStatus.error:
            return {"error": transcript.error}
        else:
            return transcript.text

    except Exception as e:
        return {"error": str(e)}