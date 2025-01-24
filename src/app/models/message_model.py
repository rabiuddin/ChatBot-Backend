from pydantic import BaseModel

class MessageRequest(BaseModel):
    ChatID: int
    HumanMessage: str
    AIMessage: str