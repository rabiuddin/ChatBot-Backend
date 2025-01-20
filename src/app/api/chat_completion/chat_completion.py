from fastapi import APIRouter, status, Request
from src.app.helper.gemini.gemini_helper import gemini_chat_completion
from src.app.helper.openai.openai_helper import openai_chat_completion
from src.app.models.prompt_model import PromptRequest
from src.app.config import Config
from src.app.utils.encryption_utils import decrypt
from src.app.utils.response_builder_utils import ResponseBuilder
from src.app.utils.limiter_utils import limiter

config = Config()

router = APIRouter()

@router.post("/")
@limiter.limit("100/minute")
def getResponse(request: Request, request_body: PromptRequest):
    response_builder = ResponseBuilder()
    try:
        # Decrypt incoming prompt
        request_body.prompt = decrypt(request_body.prompt)
        
        if request_body.prompt == "":
            return response_builder.set_success(False).set_data("Please provide a prompt.").setStatusCode(status.HTTP_400_BAD_REQUEST).build()
        elif request_body.model == "":
            return response_builder.set_success(False).set_data("Please provide a model.").setStatusCode(status.HTTP_400_BAD_REQUEST).build()
        elif request_body.model not in config.get_openai_allowed_models() and request_body.model not in config.get_gemini_allowed_models():
            return response_builder.set_success(False).set_data(f"The model you provided is not available. We only have {config.get_gemini_allowed_models() + config.get_openai_allowed_models()}").setStatusCode(status.HTTP_400_BAD_REQUEST).build()
        
        if request_body.model in config.get_openai_allowed_models():
            response = openai_chat_completion(request_body)
        elif request_body.model in config.get_gemini_allowed_models():
            response = gemini_chat_completion(request_body)
            
        return response_builder.set_success(True).set_data(response).setStatusCode(status.HTTP_200_OK).build()
    except Exception as e:
        return response_builder.set_success(False).set_data(f"Sorry Our AI services are currently down, try again later.\nExeption: {e}").setStatusCode(status.HTTP_500_INTERNAL_SERVER_ERROR).build()

