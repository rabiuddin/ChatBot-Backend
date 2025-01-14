from fastapi import APIRouter
from src.app.helper.openai_helper_folder.mergestack_helper import MergeStackService
from src.app.models.assistant_prompt_model import AssistantPrompt
from src.app.utils.encryption import encrypt, decrypt

router = APIRouter()

@router.post("/")
def getResponse(request: AssistantPrompt):
    mergestack = MergeStackService()
    try:
        # Decrypt incoming prompt
        request.prompt = decrypt(request.prompt)
        
        if request.prompt == "":
            return {"data": encrypt("Please provide a prompt.")}
            
        response = mergestack.merge_stack_assistant(request)
        return {"data": encrypt(response.content[0].text.value)}
    except Exception as e:
        return {"data": encrypt(f"Sorry Our AI services are currently down, try again later.\nExeption: {e}")}