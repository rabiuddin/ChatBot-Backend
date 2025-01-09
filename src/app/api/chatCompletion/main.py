from fastapi import APIRouter
from src.app.helper.gemini_helper_folder.gemini_helper import gemini_chat_completion
from src.app.helper.openai_helper_folder.openai_helper import openai_chat_completion
from src.app.models.prompt_model import PromptRequest
from src.app.config import Config

config = Config()

router = APIRouter()

@router.post("/")
def getResponse(request: PromptRequest):
    available_models = config.get_available_models()
    try:
        if request.prompt == "":
            return {"data": "Please provide a prompt."}
        elif request.model == "":
            return {"data": "Please provide a model."}
        elif request.model not in available_models:
            return {"data": f"The model you provided is not available. We only have {', '.join(available_models)}"}
        elif request.model == "gpt-4":
            response = openai_chat_completion(request)
        elif request.model == "gemini-1.5-flash":
            response = gemini_chat_completion(request)
        return {"data": response}
    except Exception as e:
        return {"data": f"Sorry Our AI services are currently down, try again later.\nExeption: {e}"}

