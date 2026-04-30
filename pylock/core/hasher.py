"""Password hashing and verification utilities.

Supports bcypt and argon2 algorithms."""
import bcrypt
from argon2 import PasswordHasher

ph = PasswordHasher()

def hash_password(password, algo="bcrypt"):
    """Hash a password using the specified algorithm (bcrypt or argon2)."""
    algo = str(algo).lower().strip()
    password = password.encode()

    if algo == "bcrypt":
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)
        return hashed.decode()

    elif algo == "argon2":
        return ph.hash(password.decode())

    else:
        raise ValueError(f"Unsupported algorithm:{algo}")


def verify_password(password, hashed):
    """Verify a password against a stored hash."""
    password_bytes = password.encode()

    if not hashed.startswith(("$2b$", "$argon2")):
        raise ValueError("Invalid or malformed hash (try quoting it)")

    # bcrypt
    if hashed.startswith("$2b$"):
        return bcrypt.checkpw(password_bytes, hashed.encode())

    # argon2
    elif hashed.startswith("$argon2"):
        try:
            ph.verify(hashed, password)
            return True
        except:
            return False

    else:
        raise ValueError("Unknown hash format")