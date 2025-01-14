from fastapi import APIRouter
from src.app.helper.gemini_helper_folder.gemini_helper import gemini_chat_completion
from src.app.helper.openai_helper_folder.openai_helper import openai_chat_completion
from src.app.models.prompt_model import PromptRequest
from src.app.config import Config
from src.app.utils.encryption import encrypt, decrypt

config = Config()

router = APIRouter()

@router.post("/")
def getResponse(request: PromptRequest):
    available_models = config.get_available_models()
    try:
        # Decrypt incoming prompt
        request.prompt = decrypt(request.prompt)
        
        if request.prompt == "":
            return {"data": encrypt("Please provide a prompt.")}
        elif request.model == "":
            return {"data": encrypt("Please provide a model.")}
        elif request.model not in available_models:
            return {"data": encrypt(f"The model you provided is not available. We only have {', '.join(available_models)}")}
        
        if request.model == "gpt-4":
            response = openai_chat_completion(request)
        elif request.model == "gemini-1.5-flash":
            response = gemini_chat_completion(request)
            
        return {"data": encrypt(response)}
    except Exception as e:
        return {"data": encrypt(f"Sorry Our AI services are currently down, try again later.\nExeption: {e}")}

