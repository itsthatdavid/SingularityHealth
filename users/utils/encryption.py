from cryptography.fernet import Fernet
from django.conf import settings
from base64 import b64encode, b64decode
import os

def get_encryption_key():
    """
    Obtiene la clave de encriptación desde las variables de entorno
    o genera una nueva si no existe
    """
    key = getattr(settings, 'ENCRYPTION_KEY', None)
    if not key:
        key = Fernet.generate_key()
        # En producción, esta clave debe ser almacenada de manera segura
        # y consistente, no generada dinámicamente
    return key

def encrypt_data(data: str) -> str:
    """
    Encripta datos sensibles
    """
    if not data:
        return data
    
    f = Fernet(get_encryption_key())
    encrypted_data = f.encrypt(data.encode())
    return b64encode(encrypted_data).decode()

def decrypt_data(encrypted_data: str) -> str:
    """
    Desencripta datos sensibles
    """
    if not encrypted_data:
        return encrypted_data
    
    f = Fernet(get_encryption_key())
    decrypted_data = f.decrypt(b64decode(encrypted_data))
    return decrypted_data.decode()

class EncryptedCharField:
    """
    Campo personalizado para encriptar datos en la base de datos
    """
    def __init__(self, field):
        self.field = field

    def __get__(self, instance, owner):
        if instance is None:
            return self
        encrypted_value = getattr(instance, self.field)
        if encrypted_value:
            return decrypt_data(encrypted_value)
        return encrypted_value

    def __set__(self, instance, value):
        if value:
            encrypted_value = encrypt_data(value)
            setattr(instance, self.field, encrypted_value)
        else:
            setattr(instance, self.field, value)