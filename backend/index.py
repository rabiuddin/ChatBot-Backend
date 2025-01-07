from fastapi import FastAPI
from dotenv import load_dotenv
import openai
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_SECRET_KEY")

app = FastAPI()

@app.post("/")
def indexFunction(prompt : str):
    response = openai.chat.completions.create(
    model="gpt-4", 
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    )
    assistant_message = response['choices'][0]['message']['content']
    return assistant_message