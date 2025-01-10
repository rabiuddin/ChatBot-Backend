from fastapi import APIRouter
from src.app.helper.openai_helper_folder.mergestack_helper import MergeStackService
from src.app.models.assistant_prompt_model import AssistantPrompt

router = APIRouter()

@router.post("/")
def getResponse(request: AssistantPrompt):
    mergestack = MergeStackService()
    try:
        if request.prompt == "":
            return {"data": "Please provide a prompt."}
        response = mergestack.merge_stack_assistant(request)
        return {"data": response.content[0].text.value}
    except Exception as e:
        return {"data": f"Sorry Our AI services are currently down, try again later.\nExeption: {e}"}