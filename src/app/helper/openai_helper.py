from src.app.config import Config
from src.app.models.prompt_model import PromptRequest
import openai

config = Config()

openai.api_key = config.get_openai_api_key()

def openai_chat_completion(request: PromptRequest):
    try:
        response = openai.chat.completions.create(
            model=request.model, 
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": request.prompt}
            ],
            max_tokens=int(config.get_max_tokens()),
            temperature=float(config.get_model_temperature())
        )
        assistant_message = response.choices[0].message.content

        return assistant_message
    except Exception as e:
        return f"Sorry the OpenAI services are currently down, try again later.\nException: {e}"