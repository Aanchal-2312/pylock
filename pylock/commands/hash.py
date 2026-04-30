from pylock.core.hasher import hash_password
from pylock.core.config import load_config


def handle_hash(args):
    """Handle password hashing using selected or default algorithm."""
    config = load_config()
    algo = args.algo

    # Handle missing or "none" string for algorithm selection
    if not algo or str(algo).lower() == "none":
        algo = config.get("default_algo")
    
    if not algo:
        algo = "bcrypt"

    algo = str(algo).lower().strip()

    return hash_password(args.password, algo)