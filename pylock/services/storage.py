from fileinput import filename

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import InvalidToken, Fernet
import base64
import os
import json


# 🔑 derive key from password + salt
def derive_key(password: str, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


# 🔐 encrypt full data
def encrypt_data(data, password):
    salt = os.urandom(16)
    key = derive_key(password, salt)
    f = Fernet(key)

    json_data = json.dumps(data)
    encrypted = f.encrypt(json_data.encode())

    return {
        "salt": base64.b64encode(salt).decode(),
        "data": encrypted.decode()
    }


# 🔓 decrypt
def decrypt_data(file_data, password):
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

    

# 💾 save
def save_secure(filename, data, password):
    encrypted_blob = encrypt_data(data, password)

    with open(filename, "w") as f:
        json.dump(encrypted_blob, f, indent=2)


# 📂 read + decrypt
def load_secure(filename, password):
    try:
        with open(filename, "r") as f:
            file_data = json.load(f)
    except Exception:
            raise ValueError("corrupted_file")

    # check required keys exist
    if "salt" not in file_data or "data" not in file_data:
        raise ValueError("corrupted_file")

    return decrypt_data(file_data, password)