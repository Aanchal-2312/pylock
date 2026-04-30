"""Secure Storage Utilities.
Handles encryption, decryption, and safe file storage using Fernet(AES)."""
import os
import json
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import InvalidToken, Fernet


# KEY DERIVATION
def derive_key(password: str, salt: bytes):
    """Derive a secure key from password and salt using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


# ENCRYPTION
def encrypt_data(data, password):
    """Encrypt data using a password-derived key."""
    salt = os.urandom(16)
    key = derive_key(password, salt)
    f = Fernet(key)
    
    json_data = json.dumps(data)
    encrypted = f.encrypt(json_data.encode())

    return {
        "salt": base64.b64encode(salt).decode(),
        "data": encrypted.decode()
    }


# DECRYPTION
def decrypt_data(file_data, password):
    """Decrypt stored data using the provided password."""
    salt = base64.b64decode(file_data["salt"])
    key = derive_key(password, salt)
    f = Fernet(key)

    try:
        decrypted = f.decrypt(file_data["data"].encode())
        return json.loads(decrypted.decode())
    
    except InvalidToken:
        raise ValueError("invalid_credentials")

    except Exception:
        raise ValueError("corrupted_file")

    

# FILE STORAGE
def save_secure(filename, data, password):
    """Encrypt and save data securely to a file."""
    encrypted_blob = encrypt_data(data, password)

    with open(filename, "w") as f:
        json.dump(encrypted_blob, f, indent=2)


def load_secure(filename, password):
    """Load and decrypt secure data from file."""
    try:
        with open(filename, "r") as f:
            file_data = json.load(f)
    except Exception:
        raise ValueError("corrupted_file")

    if "salt" not in file_data or "data" not in file_data:
        raise ValueError("corrupted_file")

    return decrypt_data(file_data, password)