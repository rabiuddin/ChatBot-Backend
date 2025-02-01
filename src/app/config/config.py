from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    gemini_api_key: str
    max_tokens: int
    model_temperature: float
    available_models: str
    assemblyai_api_key: str
    encryption_key: str
    IV: str
    mysql_host: str
    mysql_user: str
    mysql_password: str
    mysql_db: str
    mysql_port: int

    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.max_tokens = os.getenv("MAX_OUTPUT_TOKENS")
        self.model_temperature = os.getenv("MODEL_TEMPERATURE")
        self.assemblyai_api_key = os.getenv("ASSEMBLY_AI_API_KEY")
        self.encryption_key = bytes.fromhex(os.getenv("ENCRYPTION_KEY"))
        self.IV = bytes.fromhex(os.getenv("IV"))
        self.gemini_allowed_models = ["gemini-1.5-flash", "tunedModels/sarcastic-ai-sn3f6oecag98"]
        self.mysql_host = os.getenv("MYSQL_HOST")
        self.mysql_user = os.getenv("MYSQL_USER")
        self.mysql_password = os.getenv("MYSQL_PASSWORD")
        self.mysql_db = os.getenv("MYSQL_DATABASE")
        self.mysql_port = os.getenv("MYSQL_PORT")

    def get_gemini_api_key(self):
        return self.gemini_api_key
    
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
    
    def get_gemini_allowed_models(self):
        return self.gemini_allowed_models
    
    def get_mysql_host(self):
        return self.mysql_host
    
    def get_mysql_user(self):
        return self.mysql_user
    
    def get_mysql_password(self):
        return self.mysql_password
    
    def get_mysql_db(self):
        return self.mysql_db
    
    def get_mysql_port(self):
        return self.mysql_port
    
    