from pydantic import BaseModel

class AssistantPrompt(BaseModel):
    prompt: str