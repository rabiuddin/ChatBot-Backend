from fastapi import HTTPException
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
from src.app.config.config import Config
import base64
import json

import json
from datetime import datetime


config = Config()

# Get encryption key and IV from environment variables
ENCRYPTION_KEY = config.get_encryption_key()
IV = config.get_iv()

def default_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {obj} not serializable")

def decrypt(ciphertext: str) -> dict:
    try:
        # Decode the base64-encoded ciphertext
        encrypted_data = base64.b64decode(ciphertext)
        cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, IV)
        
        # Decrypt and unpad the datablock_size
        decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        return json.loads(decrypted.decode('utf-8'))
    except (ValueError, KeyError):
        raise HTTPException(status_code=400, detail="Invalid encryption or decryption key")

def encrypt(data: dict) -> str:
    # Convert the data to JSON
    data_json = json.dumps(data, default=default_serializer)
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, IV)
    
    # Pad the data to be AES block size compliant
    padded_data = pad(data_json.encode('utf-8'), AES.block_size)
    
    # Encrypt and encode the data in base64
    encrypted_data = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted_data).decode('utf-8')