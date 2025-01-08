from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    gemini_api_key: str
    openai_api_key: str
    max_tokens: int
    model_temperature: float
    available_models: str

    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_SECRET_KEY")
        self.max_tokens = os.getenv("MAX_OUTPUT_TOKENS")
        self.model_temperature = os.getenv("MODEL_TEMPERATURE")
        self.available_models = os.getenv("AVAILABLE_MODELS")

    def get_gemini_api_key(self):
        return self.gemini_api_key
    
    def get_openai_api_key(self):
        return self.openai_api_key
    
    def get_max_tokens(self):
        return self.max_tokens
    
    def get_model_temperature(self):
        return self.model_temperature
    
    def get_available_models(self):
        return self.available_models.split(",")