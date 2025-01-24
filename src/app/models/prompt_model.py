from pydantic import BaseModel

class PromptRequest(BaseModel):
    prompt: str
    model: str
    chatID: int
