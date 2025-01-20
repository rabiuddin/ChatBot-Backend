from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    gemini_api_key: str
    openai_api_key: str
    max_tokens: int
    model_temperature: float
    available_models: str
    assemblyai_api_key: str
    encryption_key: str
    IV: str

    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_SECRET_KEY")
        self.max_tokens = os.getenv("MAX_OUTPUT_TOKENS")
        self.model_temperature = os.getenv("MODEL_TEMPERATURE")
        self.assemblyai_api_key = os.getenv("ASSEMBLY_AI_API_KEY")
        self.encryption_key = bytes.fromhex(os.getenv("ENCRYPTION_KEY"))
        self.IV = bytes.fromhex(os.getenv("IV"))
        self.openai_allowed_models = ["gpt-4", "ft:gpt-4o-mini-2024-07-18:mergestack:sarcasm-detector:ArmuGrrw"]
        self.gemini_allowed_models = ["gemini-1.5-flash", "tunedModels/sarcastic-ai-sn3f6oecag98"]

    def get_gemini_api_key(self):
        return self.gemini_api_key
    
    def get_openai_api_key(self):
        return self.openai_api_key
    
    def get_max_tokens(self):
        return self.max_tokens
    
    def get_model_temperature(self):
        return self.model_temperature
    
    def get_assemblyai_api_key(self):
        return self.assemblyai_api_key
    
    def get_encryption_key(self):
        return self.encryption_key
    
    def get_iv(self):
        return self.IV
    
    def get_openai_allowed_models(self):
        return self.openai_allowed_models
    
    def get_gemini_allowed_models(self):
        return self.gemini_allowed_models