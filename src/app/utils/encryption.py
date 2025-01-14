from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import base64
import json
from src.app.config import Config

config = Config()

key = config.get_encryption_key().encode('utf-8')
IV = config.get_iv().encode('utf-8')

def encrypt(data: str):
    padder = padding.PKCS7(128).padder()
    cipher = Cipher(algorithms.AES(key), modes.CBC(IV))
    encryptor = cipher.encryptor()
    
    # Convert data to bytes and pad
    data_bytes = data.encode('utf-8')
    padded_data = padder.update(data_bytes) + padder.finalize()
    
    # Encrypt
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    # Encode to base64 for easy transmission
    return base64.b64encode(encrypted_data).decode('utf-8')

def decrypt(encrypted_data: str):
    unpadder = padding.PKCS7(128).unpadder()
    cipher = Cipher(algorithms.AES(key), modes.CBC(IV))
    decryptor = cipher.decryptor()
    
    # Decode from base64 and decrypt
    encrypted_bytes = base64.b64decode(encrypted_data)
    decrypted_padded = decryptor.update(encrypted_bytes) + decryptor.finalize()
    
    # Unpad and convert back to string
    decrypted_data = unpadder.update(decrypted_padded) + unpadder.finalize()
    return decrypted_data.decode('utf-8')
