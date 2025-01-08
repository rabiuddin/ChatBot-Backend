from fastapi import APIRouter
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import openai
import os

load_dotenv()

router = APIRouter()
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

class PromptRequest(BaseModel):
    prompt: str

@router.post("/")
def getResponse(request: PromptRequest):
    prompt = request.prompt

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        generation_config = genai.types.GenerationConfig(
            max_output_tokens=50,
        )
        
        response = model.generate_content(prompt)  
        
        result = response.text

        return {"data": result}
    except Exception as e:
        return {"data": f"Sorry the Gemini AI services are currently down, try again later. You asked me: {prompt}"}