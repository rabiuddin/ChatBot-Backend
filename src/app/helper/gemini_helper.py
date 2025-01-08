import google.generativeai as genai
from src.app.config import Config
from src.app.models.prompt_model import PromptRequest

config = Config()

gemini_api_key = config.get_gemini_api_key()
genai.configure(api_key=gemini_api_key)

def gemini_chat_completion(request: PromptRequest):
    try:
        model = genai.GenerativeModel(request.model)
        
        response = model.generate_content(
            request.prompt,
            generation_config = genai.GenerationConfig(
                max_output_tokens=int(config.get_max_tokens()),
                temperature=float(config.get_model_temperature()),
            )
        )  
        
        result = response.text

        return result
    except Exception as e:
        return f"Sorry the Gemini AI services are currently down, try again later.\nException: {e}"