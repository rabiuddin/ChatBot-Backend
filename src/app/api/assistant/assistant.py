from fastapi import APIRouter, status, Request
from src.app.helper.openai.mergestack_helper import MergeStackService
from src.app.models.assistant_prompt_model import AssistantPrompt
from src.app.utils.encryption_utils import decrypt
from src.app.utils.response_builder_utils import ResponseBuilder
from src.app.utils.limiter_utils import limiter

router = APIRouter()

@router.post("/")
@limiter.limit("10/minute")
def getResponse(request: Request, request_body: AssistantPrompt):
    response_builder = ResponseBuilder()
    mergestack = MergeStackService()
    try:
        # Decrypt incoming prompt
        request_body.prompt = decrypt(request_body.prompt)
        
        if request_body.prompt == "":
            return response_builder.set_success(False).set_data("Please provide a prompt.").setStatusCode(status.HTTP_400_BAD_REQUEST).build()
            
        response = (mergestack.merge_stack_assistant(request_body)).content[0].text.value
        
        return response_builder.set_success(True).set_data(response).setStatusCode(status.HTTP_200_OK).build()
    except Exception as e:
        return response_builder.set_success(False).set_data(f"Sorry Our AI services are currently down, try again later.\nExeption: {e}").setStatusCode(status.HTTP_500_INTERNAL_SERVER_ERROR).build()