from pydantic import BaseModel

class UpdateTitle(BaseModel):
    ChatID: str
    title: str