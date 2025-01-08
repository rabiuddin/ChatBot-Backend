from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv
import openai
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_SECRET_KEY")

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/")
def getResponse(request: PromptRequest):
    prompt = request.prompt
    try:
        response = openai.chat.completions.create(
        model="gpt-4", 
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        )
        assistant_message = response['choices'][0]['message']['content']
        return {"data": assistant_message}
    except Exception as e:
        return {"data": f"Sorry the OpenAI services are currectly down, try again later. You asked me: {prompt}"}