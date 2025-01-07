from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/")
def indexFunction(request: PromptRequest):
    prompt = request.prompt
    # response = openai.chat.completions.create(
    # model="gpt-4", 
    # messages=[
    #     {"role": "system", "content": "You are a helpful assistant."},
    #     {"role": "user", "content": prompt}
    # ]
    # )
    # assistant_message = response['choices'][0]['message']['content']
    return {"data": f"Hi, I am an AI assistant. How can I help you today? You asked me: {prompt}"}